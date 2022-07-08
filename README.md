# For God so loved the world, that He gave His only begotten Son, that all who believe in Him should not perish but have everlasting life
## Bible Multi Ref Maker

God is good. 

Given a new or old testament verse range, attempt to generate an interlinear HTML file.
Currently requires Diatheke from [libsword](https://crosswire.org/sword/) installed along with the TR, SpaRV1909 and OSHB modules.
It should work with any versions that use Strongs numbers.

To install required libraries
```shell
# On MacOS with Homebrew, on ubuntu use apt-get install libsword-dev for example
brew install libsword
rehash  # for ZSH to see the diatheke and installmgr executables
# If you in a country that is ok to download Bibles over the internet from, as this will contact public Internet Bible servers.
echo yes | installmgr -init
echo yes | installmgr -sc
echo yes | installmgr -r
echo yes | installmgr -ri CrossWire SpaRV1909 -ri CrossWire OSHB -ri CrossWire TR
```

```
usage: bible_interlinear_maker_chirho.py [options]

A tool to link a Bible Verse translations. Writes to STDOUT. Currently requires diatheke to be installed from libsword, along with the OSHB, TR and SpaRV1909 modules.

options:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -o OT_KEY_CHIRHO, --ot_key_chirho OT_KEY_CHIRHO
                        Old Testament key
  -n NT_KEY_CHIRHO, --nt_key_chirho NT_KEY_CHIRHO
                        New Testament key
```

```shell
# Handling chapters with different verse numberings (found so far: Genesis 32, 
# this example also does Genesis 33 after which is the same numbering in Hebrew and Other translations)
./bible_interlinear_maker_chirho.py -o "Genesis31:56-31:87 Genesis33"
```