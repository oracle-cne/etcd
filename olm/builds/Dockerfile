FROM container-registry.oracle.com/olcne/ock:base-image
COPY rpms /tmp/
RUN dnf install -y /tmp/*.rpm &&\
    dnf clean all &&\
    rm -rf /var/cache/yum/* /tmp/*.rpm

FROM container-registry.oracle.com/olcne/ock:base-image
COPY --from=0 /usr/share/licenses/etcd* /usr/share/licenses/
COPY --from=0 /usr/bin/etcdctl /usr/local/bin/etcdctl
COPY --from=0 /usr/bin/etcd /usr/local/bin/etcd
RUN test -d /LICENSES || ln -s /usr/share/licenses /LICENSES

EXPOSE 2379 2380

