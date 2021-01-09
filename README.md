# Human-ISM Fieldservice Extras

This is an Odoo 12 custom module that essentially extends `fieldservice_activity`. It generates reports based on activity and location, modifies some field names, and adds a custom field for recording numeric test results.

 Odoo module dependencies - make sure they're installed: \
	- `fieldservice` \
	- `fieldservice_activity`

# Setup

## Install
1. Download and add to your `/addons` folder
2. Go to **Apps**, search for `hism_fieldservice_extras` and install

## Use

### Orders

- Activities tab is renamed to **Tasks**
- Results/Score column for floating point values added

### Templates

- Workaround for https://github.com/OCA/field-service/issues/509

### Reporting

- Go to **Field Service > Reporting > Tasks**
- View excludes tasks that aren't `status = done`
- Can use built-in Odoo filters and date range selects

# Development

For Docker, assuming your files are in `/addons` locally :

1. `docker pull odoo:12.0`
2. `docker pull postgres:10`
3. `docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:10`
4.  `docker run -v /addons:/var/lib/odoo/addons/12.0 -p 8069:8069 --name odoo --link db:db -t odoo:12.0`
5. To look around container: `docker exec -it odoo bin/sh `