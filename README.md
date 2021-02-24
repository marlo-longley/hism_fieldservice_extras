# Human-ISM Fieldservice Extras

This is an Odoo 12 custom module that essentially extends `fieldservice_activity`. It is based off the `odoo scaffold` command for creating custom modules.
It generates reports based on activity and location, modifies some field names, and adds a custom field for recording numeric test results.

 Odoo module dependencies - make sure they're installed: \
	- `fieldservice` \
	- `fieldservice_activity`

You have to extract those modules from their parent folder on Gitub here: \
https://github.com/OCA/field-service

The `fieldservice` module itslef depends on `web_timeline` and `partner_fax` modules: \
https://apps.odoo.com/apps/modules/12.0/partner_fax/
https://apps.odoo.com/apps/modules/12.0/web_timeline/

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
- View excludes tasks that aren't `status = done` - make sure to mark the tasks as Complete in the order!
- Can use built-in Odoo filters and date range selects



# Development

For Docker, assuming your files are in `/addons` locally :

1. `docker pull odoo:12.0`
2. `docker pull postgres:10`
3. `docker run -d -e POSTGRES_USER=odoo -e POSTGRES_PASSWORD=odoo -e POSTGRES_DB=postgres --name db postgres:10`
4.  `docker run -v /addons:/var/lib/odoo/addons/12.0 -p 8069:8069 --name odoo --link db:db -t odoo:12.0`
5. To look around container: `docker exec -it odoo bin/sh `
6. On first run, you'll get an Odoo configuration screen. If using the above commands, enter Database Name option as `db`. The other options like Email and Password you can create arbitrarily. Use Demo Data if you don't plan on importing anything.
7. If this module isn't showing up in Apps, enter Development Mode, and hit "Update Apps List".

GOTCHA/Weird Stuff:
If you get this error after restarting dev server with changes:
`web.assets_backend.js:3 Uncaught TypeError: odoo.define is not a function` \
You can execute this sql command to fix: \
`DELETE FROM ir_attachment WHERE url LIKE '/web/content/%';` \
I used pgAdmin docker image to do this: 
```
docker run -p 80:80 \
    -e 'PGADMIN_DEFAULT_EMAIL=user@domain.com' \
    -e 'PGADMIN_DEFAULT_PASSWORD=SuperSecret' \
    -d dpage/pgadmin4
```
Then, use the the docker run command aboce to find db credentials.