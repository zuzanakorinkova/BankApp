#!/bin/sh
curl --ssl-reqd \
--url 'smtps://smtp-relay.sendinblue.com:465' \
--user 'zuz.korinkova@gmail.com:YOUR_SENDINBLUE_PASSWORD' \
--mail-from 'zuz.korinkova@gmail.com' \
--mail-rcpt 'zuz.korinkova@gmail.xyz' \
--upload-file mail.txt