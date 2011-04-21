# -*- coding: utf-8 -*- 

import sys
import os
import xbmc
import re
import struct

__scriptname__ = sys.modules[ "__main__" ].__scriptname__

###-------------------------  Languages  ------------------###############

LANGUAGES = (
    
    # Full Language name[0]     podnapisi[1]  ISO 639-1[2]   ISO 639-1 Code[3]   Script Setting Language[4]
    
    ("Albanian"                   , "29",       "sq",            "alb",                 "0"  ),
    ("Arabic"                     , "12",       "ar",            "ara",                 "1"  ),
    ("Belarusian"                 , "0" ,       "hy",            "arm",                 "2"  ),
    ("Bosnian"                    , "10",       "bs",            "bos",                 "3"  ),
    ("Bulgarian"                  , "33",       "bg",            "bul",                 "4"  ),
    ("Catalan"                    , "53",       "ca",            "cat",                 "5"  ),
    ("Chinese"                    , "17",       "zh",            "chi",                 "6"  ),
    ("Croatian"                   , "38",       "hr",            "hrv",                 "7"  ),
    ("Czech"                      , "7",        "cs",            "cze",                 "8"  ),
    ("Danish"                     , "24",       "da",            "dan",                 "9"  ),
    ("Dutch"                      , "23",       "nl",            "dut",                 "10" ),
    ("English"                    , "2",        "en",            "eng",                 "11" ),
    ("Estonian"                   , "20",       "et",            "est",                 "12" ),
    ("Persian"                    , "52",       "fa",            "per",                 "13" ),
    ("Finnish"                    , "31",       "fi",            "fin",                 "14" ),
    ("French"                     , "8",        "fr",            "fre",                 "15" ),
    ("German"                     , "5",        "de",            "ger",                 "16" ),
    ("Greek"                      , "16",       "el",            "ell",                 "17" ),
    ("Hebrew"                     , "22",       "he",            "heb",                 "18" ),
    ("Hindi"                      , "42",       "hi",            "hin",                 "19" ),
    ("Hungarian"                  , "15",       "hu",            "hun",                 "20" ),
    ("Icelandic"                  , "6",        "is",            "ice",                 "21" ),
    ("Indonesian"                 , "0",        "id",            "ind",                 "22" ),
    ("Italian"                    , "9",        "it",            "ita",                 "23" ),
    ("Japanese"                   , "11",       "ja",            "jpn",                 "24" ),
    ("Korean"                     , "4",        "ko",            "kor",                 "25" ),
    ("Latvian"                    , "21",       "lv",            "lav",                 "26" ),
    ("Lithuanian"                 , "0",        "lt",            "lit",                 "27" ),
    ("Macedonian"                 , "35",       "mk",            "mac",                 "28" ),
    ("Norwegian"                  , "3",        "no",            "nor",                 "29" ),
    ("Polish"                     , "26",       "pl",            "pol",                 "30" ),
    ("Portuguese"                 , "32",       "pt",            "por",                 "31" ),
    ("PortugueseBrazil"           , "48",       "pb",            "pob",                 "32" ),
    ("Romanian"                   , "13",       "ro",            "rum",                 "33" ),
    ("Russian"                    , "27",       "ru",            "rus",                 "34" ),
    ("Serbian"                    , "36",       "sr",            "scc",                 "35" ),
    ("Slovak"                     , "37",       "sk",            "slo",                 "36" ),
    ("Slovenian"                  , "1",        "sl",            "slv",                 "37" ),
    ("Spanish"                    , "28",       "es",            "spa",                 "38" ),
    ("Swedish"                    , "25",       "sv",            "swe",                 "39" ),
    ("Thai"                       , "0",        "th",            "tha",                 "40" ),
    ("Turkish"                    , "30",       "tr",            "tur",                 "41" ),
    ("Ukrainian"                  , "46",       "uk",            "ukr",                 "42" ),
    ("Vietnamese"                 , "51",       "vi",            "vie",                 "43" ),
    ("BosnianLatin"               , "10",       "bs",            "bos",                 "100"),
    ("Farsi"                      , "52",       "fa",            "per",                 "13" ),
    ("English (US)"               , "2",        "en",            "eng",                 "100"),
    ("English (UK)"               , "2",        "en",            "eng",                 "100"),
    ("Portuguese (Brazilian)"     , "48",       "pt-br",         "pob",                 "100"),
    ("Portuguese (Brazil)"        , "48",       "pb",            "pob",                 "32" ),
    ("Portuguese-BR"              , "48",       "pb",            "pob",                 "32" ),
    ("Brazilian"                  , "48",       "pb",            "pob",                 "32" ),
    ("Español (Latinoamérica)"    , "28",       "es",            "spa",                 "100"),
    ("Español (España)"           , "28",       "es",            "spa",                 "100"),
    ("Spanish (Latin America)"    , "28",       "es",            "spa",                 "100"),
    ("Español"                    , "28",       "es",            "spa",                 "100"),
    ("SerbianLatin"               , "36",       "sr",            "scc",                 "100"),
    ("Spanish (Spain)"            , "28",       "es",            "spa",                 "100"),
    ("Chinese (Traditional)"      , "17",       "zh",            "chi",                 "100"),
    ("Chinese (Simplified)"       , "17",       "zh",            "chi",                 "100") )


###-------------------------  Log  ------------------###############
   
def log(module,msg):
  xbmc.output("### [%s-%s] - %s" % (__scriptname__,module,msg,),level=xbmc.LOGDEBUG ) 

###-------------------------- match sub to file  -------------################        

def regex_tvshow(compare, file, sub = ""):
  regex_expressions = [ '[Ss]([0-9]+)[][._-]*[Ee]([0-9]+)([^\\\\/]*)$',
                      '[\._ \-]([0-9]+)x([0-9]+)([^\\/]*)',                     # foo.1x09 
                      '[\._ \-]([0-9]+)([0-9][0-9])([\._ \-][^\\/]*)',          # foo.109
                      '([0-9]+)([0-9][0-9])([\._ \-][^\\/]*)',
                      '[\\\\/\\._ -]([0-9]+)([0-9][0-9])[^\\/]*',
                      'Season ([0-9]+) - Episode ([0-9]+)[^\\/]*',
                      '[\\\\/\\._ -][0]*([0-9]+)x[0]*([0-9]+)[^\\/]*',
                      '[[Ss]([0-9]+)\]_\[[Ee]([0-9]+)([^\\/]*)',                 #foo_[s01]_[e01]
                      '[\._ \-][Ss]([0-9]+)[\.\-]?[Ee]([0-9]+)([^\\/]*)',        #foo, s01e01, foo.s01.e01, foo.s01-e01
                      '[Ss]([0-9]+)[][ ._-]*[Ee]([0-9]+)([^\\\\/]*)$',
                      '[\\\\/\\._ \\[\\(-]([0-9]+)x([0-9]+)([^\\\\/]*)$'
                      ]
  sub_info = ""
  tvshow = 0
  
  for regex in regex_expressions:
    response_file = re.findall(regex, file)                  
    if len(response_file) > 0 : 
      print "Regex File Se: %s, Ep: %s," % (str(response_file[0][0]),str(response_file[0][1]),)
      tvshow = 1
      if not compare :
        title = re.split(regex, file)[0]
        for char in ['[', ']', '_', '(', ')','.','-']: 
           title = title.replace(char, ' ')
        if title.endswith(" "): title = title[:-1]
        return title,response_file[0][0], response_file[0][1]
      else:
        break
  
  if (tvshow == 1):
    for regex in regex_expressions:       
      response_sub = re.findall(regex, sub)
      if len(response_sub) > 0 :
        try :
          sub_info = "Regex Subtitle Ep: %s," % (str(response_sub[0][1]),)
          if (int(response_sub[0][1]) == int(response_file[0][1])):
            return True
        except: pass      
    return False
  if compare :
    return True
  else:
    return "","",""    



def languageTranslate(lang, lang_from, lang_to):
  for x in LANGUAGES:
    if lang == x[lang_from] :
      return x[lang_to]


      
