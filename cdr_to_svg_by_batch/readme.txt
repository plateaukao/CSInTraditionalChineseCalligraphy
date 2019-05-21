Is there exists a open-source library of python to convert the .CDR files to .SVG files?
Imagemagick

1. https://imagemagick.org/script/download.php#macosx (Install method)

But Imagemagick does not support this CDR format.

identify -list format

2. UniConvertor is a universal vector graphics translator. It is a command line tool which uses sK1 object model to convert one format to another.

https://sk1project.net/modules.php?name=Products&product=uniconvertor

Import Filters:

    CorelDRAW ver.7-X3,X4 (CDR/CDT/CCX/CDRX/CMX)
    Adobe Illustrator up to 9 ver. (AI postscript based)
    Postscript (PS)
    Encapsulated Postscript (EPS)
    Computer Graphics Metafile (CGM)
    Windows Metafile (WMF)
    XFIG
    Scalable Vector Graphics (SVG)
    Skencil/Sketch/sK1 (SK and SK1)
    Acorn Draw (AFF)

output filters:

    AI (Postscript based Adobe Illustrator 5.0 format)
    SVG (Scalable Vector Graphics)
    SK (Sketch/Skencil format)
    SK1 (sK1 format)
    CGM (Computer Graphics Metafile)
    WMF (Windows Metafile)
    PDF (Portable Document Format)
    PS (PostScript)


sK1 2.0 is professional quality illustration program for Windows, GNU/Linux and macOS platforms. （https://sk1project.net）




https://listoffreeware.com/best-free-mac-cdr-viewer-software/

4 Best Free MAC CDR Viewer Software



====== last use inkspace


/Applications/Inkscape.app/Contents/Resources/bin/inkscape-bin -z -D --file=test.cdr --export-plain-svg=test.svg --export-latex

