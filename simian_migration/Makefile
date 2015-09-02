USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=simian_migrate_bootstrap
PACKAGE_NAME=simian_migrate_bootstrap
REVERSE_DOMAIN=org.reallifechurch
PAYLOAD=\
    pack-script\
	pack-Library-LaunchDaemons-org.reallifechurch.simian_migrate_bootstrap.plist \

pack-script:
	@sudo mkdir -p ${WORK_D}/usr/local/simian_migrate/
	@sudo ${CP} puppet_bootstrap ${WORK_D}/usr/local/simian_migrate/simian_migrate_bootstrap
	@sudo chmod 700 ${WORK_D}/usr/local/simian_migrate/simian_migrate_bootstrap
