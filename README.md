# Twilio Texting

The Python script to send SMS messages with [twilio](https://www.twilio.com) service.

Can be used together with [Snort Alert Log Reader](https://github.com/goooroooX/snort_reader).

Main features:
* take input parameters as SMS text lines
* send SMS

NOTE: twilio account is required (trial account is OK as well).

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

```
Python 2.7  (Python 2.6 is not supported)
CentOS 7    (tested)
Windows 10  (tested)
```

### Installing

Download and copy files, set executable flag, create symlink (optional):

```
mkdir /opt/texting
cp texting.py /opt/texting/
cp -r cert /opt/texting/
cp -r lib /opt/texting/
chmod +x /opt/texting/texting.py
ln -s /opt/texting/texting.py /opt/texting/texting
```

### Configuring

Log in to your twilio account, and find following information:
* phone number you will use to send SMS
* SID
* token

Open script for editing:

```
vim /opt/texting/texting.py
```

Update following variables:
* PHONE_NUMBERS - mobile number(s) to send SMS (sould be configured in twilio as well)
* FROM          - twilio phone number
* SID           - account SID
* TOKEN         - twilio API token

### Testing

Execute script with parameters and check the log file:

```
/opt/texting/texting.py "first SMS line" "second line"
cat /var/log/alert_texting.log
```

### Notes

The folder 'cert' contains twilio sertificate extracted from [official twilio wheel](https://pypi.python.org/pypi/twilio) package (twilio.conf).

## Authors

* **Dmitry Nikolaenya** - *texting code* - [gooorooo.com](https://gooorooo.com)

## License

This project is licensed under the Apache 2.0 License - see the [LICENSE.md](LICENSE.md) file for details.
