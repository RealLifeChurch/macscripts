USE_PKGBUILD=1
include /usr/local/share/luggage/luggage.make

TITLE=simian_migrate_bootstrap
PACKAGE_NAME=10-9_Undergrounds
REVERSE_DOMAIN=org.reallifechurch
PAYLOAD=\
    pack-script \

pack-script:
	@sudo mkdir -p ${WORK_D}/usr/local/facts/
	@sudo ${CP} deployment_type.txt ${WORK_D}/usr/local/facts/deployment_type.txt
