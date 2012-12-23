# RoboFont Script
# Install current font with empty glyphs. It is useful when you are testing font in InDesign 
# Alexander Lubovenko
# http://github.com/typedev

from robofab.world import CurrentFont


s = 'space exclam quotesingle quotedbl numbersign dollar percent ampersand parenleft parenright asterisk plus comma hyphen period slash zero one two three four five six seven eight nine colon semicolon less equal greater question at A B C D E F G H I J K L M N O P Q R S T U V W X Y Z bracketleft backslash bracketright asciicircum underscore grave a b c d e f g h i j k l m n o p q r s t u v w x y z braceleft bar braceright asciitilde exclamdown cent sterling currency yen brokenbar section dieresis copyright ordfeminine guillemotleft logicalnot registered macron degree plusminus twosuperior threesuperior acute mu paragraph periodcentered cedilla onesuperior ordmasculine guillemotright onequarter onehalf threequarters questiondown Agrave Aacute Acircumflex Atilde Adieresis Aring AE Ccedilla Egrave Eacute Ecircumflex Edieresis Igrave Iacute Icircumflex Idieresis Eth Ntilde Ograve Oacute Ocircumflex Otilde Odieresis multiply Oslash Ugrave Uacute Ucircumflex Udieresis Yacute Thorn germandbls agrave aacute acircumflex atilde adieresis aring ae ccedilla egrave eacute ecircumflex edieresis igrave iacute icircumflex idieresis eth ntilde ograve oacute ocircumflex otilde odieresis divide oslash ugrave uacute ucircumflex udieresis yacute thorn ydieresis dotlessi circumflex caron breve dotaccent ring ogonek tilde hungarumlaut quoteleft quoteright minus u00A0|00A0 afii10017 afii10018 afii10019 afii10020 afii10021 afii10022 afii10023 afii10024 afii10025 afii10026 afii10027 afii10028 afii10029 afii10030 afii10031 afii10032 afii10033 afii10034 afii10035 afii10036 afii10037 afii10038 afii10039 afii10040 afii10041 afii10042 afii10043 afii10044 afii10045 afii10046 afii10047 afii10048 afii10049 afii10065 afii10066 afii10067 afii10068 afii10069 afii10070 afii10071 afii10072 afii10073 afii10074 afii10075 afii10076 afii10077 afii10078 afii10079 afii10080 afii10081 afii10082 afii10083 afii10084 afii10085 afii10086 afii10087 afii10088 afii10089 afii10090 afii10091 afii10092 afii10093 afii10094 afii10095 afii10096 afii10097 afii10051 afii10099 afii10050 afii10055 afii10052 afii10100 afii10103 afii10098 afii10057 afii10053 afii10101 afii10056 afii10104 afii10058 afii10106 afii10059 afii10107 afii10105 afii10054 afii10060 afii10108 afii10061 afii10109 afii10102 afii10062 afii10110 afii10145 afii10193 afii61352'

ng = s.split(' ')

font = CurrentFont()

for gname in ng:
    if gname not in font.keys():
        d = RGlyph()
        font[gname] = d
        missglyph = font[gname]
        missglyph.width = 0
        missglyph.update()

font.update()

font.testInstall()

glyphOrder = font.glyphOrder

for gname in ng:
    if font[gname].width == 0:
         font.removeGlyph(gname)
         
font.glyphOrder = glyphOrder                
font.update()    
