# Fix-sub
Script for shifting the times from a .srt file. 

## Usage
To run the script, write the following command:

```bash
fix-sub.py <srt-file-name> <mode> <shifting-constant> [options]
```

The **"shifting-constant"** parameter must be an integer or a double value.

The **mode** parameter must be *-f* (forward subtitles) or *-b* (slow down subtitles)

In **[options]** you can specify the subtitles that you want to **exclude** or **include** by writing *-e* or *-i* followed by the subtitle numbers:

```bash
-e [1,3,56]		'shift all except 1,3,56'
-e [2:8]		'shift all except from 2 to 8 (included)'
-i [:45]		'only shift from the start to 8 (included)'
-i [4:]			'only shift from 4 to the last one (included)'
```

Some examples:

```bash
fix-sub.py subtitles.py -b 0.567  		'slow down all subtitles by 0.567'

fix-sub.py subtitles.py -f 0.567 -e [456]	'forward all subtitles except 456'
```

If you exceed the length of the number of subtitles, it won't shift the last one




