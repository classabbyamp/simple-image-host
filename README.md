# simple-image-host

This is an *exceedingly* simple app.

* User authentication via HTTP basic auth
* Web upload (for registered users only)
    * visit `{domain}/` for this
* File type and size restrictions
    * You can bypass the upload restrictions by using a docker volume and uploading to the host server
* Direct links to uploaded files
    * `{domain}/{filename}`

## Example `conf.py`

```py
#!/usr/bin/env python3

# maximum filesize for uploads
max_filesize = 50 * 1024 * 1024

# users and passwords (passwords will be hashed later)
users_pt = {
        "admin": "password",
        "user": "hunter2",
    }

# the folder in which to store the images
upload_folder = "images"

# valid extensions for uploaded files
exts = {
        "jpg",
        "jpeg",
        "png",
        "gif",
    }
```

## Example `docker-compose.yml`

Make sure to create `conf.py` in the `data` directory.

```yaml
version: "3"

services:
    host:
    image: "docker.pkg.github.com/classabbyamp/simple-image-host/simple-image-host:latest"
        restart: on-failure
        volumes:
            - "./data:/app/data:ro"
            - "./images:/app/images:rw"
```
