FROM loadimpact/k6:latest
ENV SCRIPT sample.js
COPY ./test /test
WORKDIR /test
# Override the entry point of the base k6 image
ENTRYPOINT []
CMD ["sh", "-c", "k6 run --out statsd $SCRIPT"]