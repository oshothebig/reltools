# Pull base image.
FROM libero18/ubuntu-14.04:auto

ADD libip4tc.so.0 /usr/local/libip4tc.so.0
ADD asicd.conf /usr/local/asicd.conf
ADD gen_image.sh /usr/local/bin/gen_image.sh
ADD flex.deb /usr/local/flex.deb
RUN chmod +x /usr/local/bin/gen_image.sh

CMD sh /usr/local/bin/gen_image.sh
