# github_data_stream

This class is used to stream data from Github. It can stream commits, issues and pull requests, by calling the read() method repeatedly to get the next batch of data.
  When the first resource is depleted it will return the next resource and so on until all resources are depleted for the current repo, then it will go to the next repo. When there is no more data it will return None.
  If an error occurred in getting the commits, issues or pull requests the error will be returned. If an error occurred in getting a single commit it will try to get the next one.
  The API can do 60 requests per hour, limited by Github.
The constructor accepts 3 arguments:
  -owner of type string
  -repo of type list of strings, this is the repository list
  -resources of type list of strings, it can contain only this values: "commits", "issues", "pull_requests"
Example:
  object = GitHub("octokit", ["core.js"], ["issues","commits"])
