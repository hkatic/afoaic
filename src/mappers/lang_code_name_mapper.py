from typing import Dict, List, Union

def map_language_code_name(input: str) -> Union[str, None]:
	language_map: Dict[str, str] = {
		"auto": _("Auto detect"),
		"af": _("Afrikaans"),
		"ar": _("Arabic"),
		"hy": _("Armenian"),
		"az": _("Azerbaijani"),
		"be": _("Belarusian"),
		"bs": _("Bosnian"),
		"bg": _("Bulgarian"),
		"ca": _("Catalan"),
		"zh": _("Chinese"),
		"hr": _("Croatian"),
		"cs": _("Czech"),
		"da": _("Danish"),
		"nl": _("Dutch"),
		"en": _("English"),
		"et": _("Estonian"),
		"fi": _("Finnish"),
		"fr": _("French"),
		"gl": _("Galician"),
		"de": _("German"),
		"el": _("Greek"),
		"he": _("Hebrew"),
		"hi": _("Hindi"),
		"hu": _("Hungarian"),
		"is": _("Icelandic"),
		"id": _("Indonesian"),
		"it": _("Italian"),
		"ja": _("Japanese"),
		"kn": _("Kannada"),
		"kk": _("Kazakh"),
		"ko": _("Korean"),
		"lv": _("Latvian"),
		"lt": _("Lithuanian"),
		"mk": _("Macedonian"),
		"ms": _("Malay"),
		"mr": _("Marathi"),
		"mi": _("Maori"),
		"ne": _("Nepali"),
		"no": _("Norwegian"),
		"fa": _("Persian"),
		"pl": _("Polish"),
		"pt": _("Portuguese"),
		"ro": _("Romanian"),
		"ru": _("Russian"),
		"sr": _("Serbian"),
		"sk": _("Slovak"),
		"sl": _("Slovenian"),
		"es": _("Spanish"),
		"sw": _("Swahili"),
		"sv": _("Swedish"),
		"tl": _("Tagalog"),
		"ta": _("Tamil"),
		"th": _("Thai"),
		"tr": _("Turkish"),
		"uk": _("Ukrainian"),
		"ur": _("Urdu"),
		"vi": _("Vietnamese"),
		"cy": _("Welsh"),
	}
	# Create a reverse mapping for language names to codes
	reverse_map = {v: k for k, v in language_map.items()}
	if input in language_map:
		return language_map[input]
	elif input in reverse_map:
		return reverse_map[input]
	elif input == "LIST_LANGUAGE_NAMES":
		return sorted(language_map.values())
	else:
		return None

def get_language_names() -> List[str]:
	return map_language_code_name("LIST_LANGUAGE_NAMES")
    