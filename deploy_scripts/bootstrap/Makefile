
USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=puppet_bootstrap
PACKAGE_NAME=deploy_bootstrap
REVERSE_DOMAIN=org.reallifechurch
PAYLOAD=\
    pack-script \
		pack-Library-LaunchDaemons-org.reallifechurch.deploy_bootstrap.plist

pack-script:
	@sudo mkdir -p ${WORK_D}/usr/local/deploy-scripts/bootstrap
	@sudo ${CP} deploy_bootstrap ${WORK_D}/usr/local/deploy-scripts/bootstrap/deploy_bootstrap
	@sudo chmod 700 ${WORK_D}/usr/local/deploy-scripts/bootstrap/deploy_bootstrap
