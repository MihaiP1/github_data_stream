import requests as req
from requests import exceptions
from requests.auth import HTTPBasicAuth
from ratelimit import limits


class GitHub:
    """This class is used to stream data from Github. It can stream commits, issues and pull requests,
     by calling the read() method repeatedly to get the next batch of data.
    When the first resource is depleted it will return the next resource and so on until all resources
    are depleted for the current repo, then it will go to the next repo. When there is no more data it will return None.
    If an error occurred in getting the commits, issues or pull requests the error will be returned.
    If an error occurred in getting a single commit it will try to get the next one.
    The API can do 60 requests per hour, limited by Github.
    The constructor accepts 3 arguments:
    -owner of type string
    -repo of type list of strings, this is the repository list
    -resources of type list of strings, it can contain only this values: "commits", "issues", "pull_requests"
    Example:
        object = GitHub("octokit", ["core.js"], ["issues","commits"])"""

    git_url = "https://api.github.com/repos/"
    git_call_limit = 60  # Limited by github for unauthenticated users
    git_time_limit_in_seconds = 3600

    def __init__(self, owner, repo, resources):
        self.owner = owner
        self.repo = repo
        self.resources = resources

        self.__current_repo = 0

        self.__commits = None
        self.__issues = None
        self.__pull_requests = None

    @limits(calls=git_call_limit, period=git_time_limit_in_seconds)
    def read(self):
        while self.__current_repo < len(self.repo):
            if "commits" in self.resources:
                if not self.__commits:
                    try:
                        self.__commits = req.get(self.git_url +
                                                 self.owner + "/" +
                                                 self.repo[self.__current_repo] +
                                                 "/commits")
                        self.__commits.raise_for_status()
                        return self.__get_commits_for_current_page()
                    except exceptions.RequestException as e:
                        self.__commits = None
                        print(e)
                        return e
                elif "next" in self.__commits.links:
                    try:
                        self.__commits = req.get(self.__commits.links["next"]["url"])
                        self.__commits.raise_for_status()
                        return self.__get_commits_for_current_page()
                    except exceptions.RequestException as e:
                        self.__commits = None
                        print(e)
                        return e

            if "issues" in self.resources:
                if not self.__issues:
                    try:
                        self.__issues = req.get(self.git_url +
                                                self.owner + "/" +
                                                self.repo[self.__current_repo] +
                                                "/issues")
                        self.__issues.raise_for_status()
                        return self.__issues.json()
                    except exceptions.RequestException as e:
                        self.__issues = None
                        print(e)
                        return e
                elif "next" in self.__issues.links:
                    try:
                        self.__issues = req.get(self.__issues.links["next"]["url"])
                        self.__issues.raise_for_status()
                        return self.__issues.json()
                    except exceptions.RequestException as e:
                        self.__issues = None
                        print(e)
                        return e

            if "pull_requests" in self.resources:
                if not self.__pull_requests:
                    try:
                        self.__pull_requests = req.get(self.git_url +
                                                       self.owner + "/" +
                                                       self.repo[self.__current_repo] +
                                                       "/pulls")
                        self.__pull_requests.raise_for_status()
                        return self.__pull_requests.json()
                    except exceptions.RequestException as e:
                        self.__pull_requests = None
                        print(e)
                        return e
                elif "next" in self.__pull_requests.links:
                    try:
                        self.__pull_requests = req.get(self.__pull_requests.links["next"]["url"])
                        self.__pull_requests.raise_for_status()
                        return self.__pull_requests.json()
                    except exceptions.RequestException as e:
                        self.__pull_requests = None
                        print(e)
                        return e
            self.__current_repo += 1
            self.__commits = None
            self.__issues = None
            self.__pull_requests = None
        return None

    def __get_commits_for_current_page(self):
        commit_list = []
        for commit in self.__commits.json():
            try:
                commit_list.append(self.get_commit(commit["sha"]))
            except exceptions.RequestException as e:
                print(e)
                continue

        return commit_list

    @limits(calls=git_call_limit-1, period=git_time_limit_in_seconds)
    def get_commit(self, commit_sha):
        return req.get(self.git_url +
                       self.owner + "/" +
                       self.repo[self.__current_repo] +
                       "/commits/" +
                       commit_sha).json()
