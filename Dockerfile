ARG BUILDPLATFORM=linux/amd64
ARG BUILDTAG=3-alpine
FROM --platform=${TARGETPLATFORM:-linux/amd64} ghcr.io/openfaas/of-watchdog:0.9.10 as watchdog


FROM --platform=$BUILDPLATFORM python:$BUILDTAG as base_build

WORKDIR /home/user/app

COPY function/handler handler
COPY function/tests tests
COPY function/features features
COPY function/pyproject.toml .
COPY function/poetry.lock .
COPY function/README.md .
COPY function/.pre-commit-config.yaml .
COPY function/.flake8 .

ENV PATH=$PATH:/home/user/.local/bin

FROM base_build as test

ARG TESTBUILD=True
ENV TESTBUILD=$TESTBUILD

RUN pip install --no-cache poetry poethepoet
RUN poetry config --no-cache
RUN poe install-dev
RUN poetry build --format=wheel
RUN poetry export --only main -f requirements.txt --without-hashes --output requirements.txt
RUN if [ "$TESTBUILD" = 'True' ]; then poe test; fi

ENTRYPOINT ["poe", "-q"]
CMD ["test"]

FROM --platform=$BUILDPLATFORM python:$BUILDTAG as prod

COPY --from=watchdog /fwatchdog /usr/bin/fwatchdog
RUN chmod +x /usr/bin/fwatchdog

RUN addgroup --system user && adduser --system user --ingroup user
USER user

WORKDIR /home/user/app

COPY --chown=user:user --from=test /home/user/app/requirements.txt requirements.txt
COPY --chown=user:user --from=test /home/user/app/dist dist

RUN pip install --no-cache -r requirements.txt dist/*.whl --user

# ENV fprocess="poetry run server"
ENV fprocess="poetry run server"

ENV cgi_headers="true"
ENV mode="http"
ENV upstream_url="http://127.0.0.1:8000"
ENV write_debug="false"

HEALTHCHECK --interval=5s CMD [ -e /tmp/.lock ] || exit 1

CMD ["fwatchdog"]


# ENTRYPOINT ["python", "-m"]
# CMD ["handler.handler"]

