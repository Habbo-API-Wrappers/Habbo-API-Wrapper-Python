# Wired API Python

A  Python wrapper for the Habbo public API.

## Installation

Install from source (this package is not yet published to PyPI):

```bash
pip install -e .
```

or install the only runtime dependency directly:

```bash
pip install -r requirements.txt
```

## Basic Usage

### Initializing the API Client

```python
from wired_api_python import HabboPublicAPI, Hotel

# Create an instance targeting the .COM hotel
api = HabboPublicAPI.from_hotel(Hotel.COM)
```

### Accessing Standard Endpoints

Once instantiated, use the resource methods to query public data, for example:

```python
# Fetch the achievements list
achievements = api.achievements().all()

# Fetch room details by ID
room = api.rooms().by_id(room_id)
```

## Wired Variables Endpoints

To interact with WIRED variables, call `.variables()` on your API instance with
the room ID and your read/write keys:

```python
var_api = api.variables(room_id, wired_read_key, wired_write_key)

# Access variable data for the specified room
all_var_names = var_api.list_all()
user_var_profile = var_api.user().get_profile_by_username("WiredSpast")
```

## Error Handling

API requests raise `HabboApiException` on failure. Wrap your calls in a
`try`/`except` block:

```python
from wired_api_python import HabboApiException

try:
    room = api.rooms().by_id(room_id)
except HabboApiException as e:
    # Handle API-specific errors (e.g., 404 Not Found, 500 Server Error)
    print(e.code, e.response_body)
```

## Supported Feature Overview

- **Public Endpoints**:
  - Achievements -- `api.achievements()`
  - Badge owner count -- `api.badges()`
  - Groups -- `api.groups()`
  - Marketplace statistics -- `api.marketplace()`
  - Ping -- `api.ping()`
  - Rooms -- `api.rooms()`
  - Lists (hot looks) -- `api.lists()`
  - Users -- `api.users()`
- **Variable Endpoints** (`api.variables(room_id, read_key, write_key)`):
  - Read and manage permanent user variables -- `.user()`
  - Read and manage permanent furni variables -- `.furni()`
  - Read and manage permanent global variables -- `.global_()`