from typing import Dict, List, Union

def map_output_format_code_name(input: str) -> Union[str, None]:
	format_map: Dict[str, str] = {
		"text": _("simple text"),
		"srt": _("subrip subtitles (srt)"),
		"vtt": _("video text track subtitles (vtt)"),
	}
	# Create a reverse mapping for output format names to codes
	reverse_map = {v: k for k, v in format_map.items()}
	if input in format_map:
		return format_map[input]
	elif input in reverse_map:
		return reverse_map[input]
	elif input == "LIST_FORMAT_NAMES":
		return sorted(format_map.values())
	else:
		return None

def get_output_format_names() -> List[str]:
	return map_output_format_code_name("LIST_FORMAT_NAMES")
        