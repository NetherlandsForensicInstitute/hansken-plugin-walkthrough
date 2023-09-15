# IOS knowledgeC.db battery events plugin

This repository is the solution to the [Hansken.io 2023](https://www.hansken.nl/latest/events/2023/09/20/hansken.io-2023) workshop
 "Extraction Plugin Walkthrough"

To get started with a new plugin:
* Read the [extraction plugin SDK documentation](https://netherlandsforensicinstitute.github.io/hansken-extraction-plugin-sdk-documentation/latest/)
* Find the [Python plugin template](https://github.com/NetherlandsForensicInstitute/hansken-extraction-plugin-template-python)


## Plugin card

| Part 1                      |                                                                                                        |
|-----------------------------|--------------------------------------------------------------------------------------------------------|
| Validation report           | Not available                                                                                          |
| Code quality level          | Dev ready                                                                                              |
| External dependencies       | n/a                                                                                                    |
| Test results                | Test data from Crystal Clear demo case, results are present in plugin, but were not manually validated |
| **Part 2**                  |                                                                                                        |
| Plugin name and version     | hansken.org/extract/ios/battery-level                                                                  |
| release notes               | n/a                                                                                                    |
| creator                     | NFI; [Remco](mailto:remco@holmes.nl)                                                                   |
| matcher                     | file.name=knowledgeC.db AND $data.fileType=\'SQLite 3\'                                                |
| overview of data/metadata   | Reads data, marks knowledgeC.db as `eventLog`, and creates child traces of type `event`                |
| applied algorithms          | n/a                                                                                                    |
| Available reference data    | Included as test data                                                                                  |
| **Part 3**                  |                                                                                                        |
| Intended use                | Hansken.io 2023 plugin walkthrough                                                                     |
| Ethical considerations      | t.b.d.                                                                                                 |
| Caveats                     | The results are far from perfect                                                                       |
| Recommendations             | DO NOT USE THIS PLUGIN IN AN ACTUAL CASE!                                                              |

_(end of Hansken plugin card)_


## For developers

Tox commands that may be useful:
* `tox`: runs your tests
* `tox -e integration-test`: runs your tests against the packaged version of your plugin (requires Docker)
* `tox -e regenerate`: regenerates the expected test results (use after you update your plugin)
* `tox -e upgrade`: regenerates `requirements.txt` from [`requirements.in`](requirements.in)
* `tox -e package`: creates a extraction plugin OCI/Docker image that can be published to Hansken (requires Docker)

Note: see the readme text in the [`Dockerfile`](Dockerfile) if you need to set proxies or private Python package registries for building a plugin.
