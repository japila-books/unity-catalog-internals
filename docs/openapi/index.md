# OpenAPI

Unity Catalog API is described by the following OpenAPI specifications:

Title | Server URLs | File
-|-|-
 Unity Catalog API | <http://localhost:8080/api/2.1/unity-catalog> | [api/all.yaml]({{ uc.github }}/api/all.yaml)
 Unity Control API | <http://localhost:8080/api/1.0/unity-control> | [api/control.yaml]({{ uc.github }}/api/control.yaml)

The OpenAPI specifications are used at build time by [OpenAPI Generator]({{ openapi.home }}) to auto-generate Java classes.

[sbt-openapi-generator]({{ openapi.github }}/sbt-openapi-generator) 7.9.0 is used in the following sbt modules:

* `target/clients/java`
* `target/control/java`
* `clients/python/target` (copied to `clients/python/target/src/unitycatalog)`
* `server/target/controlmodels`
* `server/target/models`

??? note "Thanks for using OpenAPI Generator"
    You should see the following message at build time for every sbt module that generates required classes based on the OpenAPI spec:

    ```text
    ################################################################################
    # Thanks for using OpenAPI Generator                                           #
    # Please consider donation to help us maintain this project 🙏                 #
    # <https://opencollective.com/openapi_generator/donate>                        #
    ################################################################################
    ```
