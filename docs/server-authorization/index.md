# Server Authorization

**Server Authorization** can be enabled in [Unity Catalog Server](../server/index.md) using `server.authorization` property in `etc/conf/server.properties` configuration file.

To enable the server authorization `server.authorization` property should be `enable` (case-insensitive).

With server authorization enabled, Unity Catalog Server registers [AuthDecorator](AuthDecorator.md) to intercept all requests to `/api/2.1/unity-catalog/`-prefixed URLs.
