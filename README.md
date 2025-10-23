# Purrify

[English](README.md) | [中文](README.zh.md)

[HashCat](https://github.com/hashcat/hashcat) mask generator for mobile phone numbers based on libphonenumber metadata, inspired by [Felinize](https://github.com/Arnie97/felinize/).

Creates `.hcmask` files with all mobile phone numbers in specified cities, according to the [`ranges.csv` metadata provided by libphonenumber][1].

## Installation

Download phone number ranges provided by [libphonenumber](https://github.com/google/libphonenumber):

```
curl -#LO https://github.com/google/libphonenumber/raw/master/metadata/metadata.zip
unzip -j metadata.zip metadata/86/ranges.csv
```

> **Note:** The `86` in the path represents China's country calling code. You can replace it with other country codes as needed (e.g., `1` for USA/Canada, `44` for UK, `81` for Japan, etc.).

Install Purrify using [UV](https://github.com/astral-sh/uv):

```
uv tool install git+https://github.com/13m0n4de/purrify
```

## Usage

Specify one or more city names in Chinese, English, or other languages:

```
uvx purrify 南京 shanghai < ranges.csv > phones.hcmask
hashcat -a 3 -m 13000 rar.hash phones.hcmask
```

If you need a wordlist file, you can generate one from the `.hcmask` file using hashcat:

```
hashcat -a 3 --stdout phones.hcmask > phones.list
```

[1]: https://github.com/google/libphonenumber/blob/master/metadata/metadata.zip
