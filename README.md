# Composer Plugin for edyan/stakkr
Plugin made by Inet Process to run [composer](https://getcomposer.org) commands

__WARNING: The plugin directory must be named `composer`__ (complete path: plugins/composer)

# Installation
From `stakkr` root :

```bash
$ cd plugins
$ git clone https://github.com/edyan/stakkr-composer composer
$ stakkr refresh-plugins
```


# composer commands
Use `stakkr composer` to use composer. On the first run, composer is downloaded. You can define the version at this stage or keep 1.4.2 and then run a `stakkr composer self-update`

Example to update packages
```bash
cd www/project
stakkr composer update
```
