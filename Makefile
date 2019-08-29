PLAT=manylinux1_x86_64
DOCKER_IMAGE=quay.io/pypa/manylinux2010_x86_64
PRE_CMD=
docker-wheels:
	docker run --rm -e PLAT=${PLAT} -v `pwd`:/io ${DOCKER_IMAGE} ${PRE_CMD} /io/build_wheels.sh
	auditwheel repair /output/mylibrary*whl -w /output
	
install:
	docker pull ${DOCKER_IMAGE}
