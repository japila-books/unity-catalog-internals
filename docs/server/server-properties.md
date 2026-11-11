# Server Properties

Unity Catalog defines a `Property` public enum for the supported server properties.

## server.authorization { #AUTHORIZATION_ENABLED }

Default: `disable`

Allowed values:

* `enable`
* `disable`

Used when:

* `ServerProperties` is requested to [isAuthorizationEnabled](ServerProperties.md#isAuthorizationEnabled)
