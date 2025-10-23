# Purrify

[English](README.md) | [中文](README.zh.md)

基于 libphonenumber 元数据的手机号码 [HashCat](https://github.com/hashcat/hashcat) 掩码生成器，灵感来自 [Felinize](https://github.com/Arnie97/felinize/)。

根据 [libphonenumber 提供的 `ranges.csv` 元数据][1]，为指定城市的所有手机号码创建 `.hcmask` 文件。

## 安装

下载 [libphonenumber](https://github.com/google/libphonenumber) 提供的手机号段数据：

```
curl -#LO https://github.com/google/libphonenumber/raw/master/metadata/metadata.zip
unzip -j metadata.zip metadata/86/ranges.csv
```

> **注意：** 路径中的 `86` 代表中国的国际区号。你可以根据需要替换为其他国家的区号（例如 `1` 代表美国/加拿大，`44` 代表英国，`81` 代表日本等）。

使用 [UV](https://github.com/astral-sh/uv) 安装 Purrify：

```
uv tool install git+https://github.com/13m0n4de/purrify
```

## 使用

指定一个或多个城市名称，可以使用中文、英文或其他语言：

```
uvx purrify 南京 shanghai < ranges.csv > phones.hcmask
hashcat -a 3 -m 13000 rar.hash phones.hcmask
```

如果需要一份字典文件，可以用 hashcat 从 `.hcmask` 文件生成：

```
hashcat -a 3 --stdout phones.hcmask > phones.list
```

[1]: https://github.com/google/libphonenumber/blob/master/metadata/metadata.zip
