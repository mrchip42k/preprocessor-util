# This program is a wrapper for convenience to a command like this:
# echo O_APPEND | gcc -include fcntl.h -E - | more
# python3.6 preproc.py O_APPEND fnctl.h

import sys
import os
import subprocess

#### SETTINGS ####

CC = "gcc"

TRY_USE_BAT = True

DEFAULT_INCLUDES = [
	"stdio.h",
	"stdbool.h",
	"stdlib.h",
	"unistd.h",
	"string.h",
]

#### -------- ####


# This marker is used to remove any included code from the output,
# and only display the expanded macros given as the first argument to this program.
# Preproc seems to delete comments and defines, a global constant seems remain untouched.
MARKER = "const int PREPROC_CONTENT_MARKER = 69420;"


def arg_error():
	print("Expected arguments: <code to preprocess> <header> <another_header...>")
	sys.exit(1)


def get_includes():
	if len(sys.argv) < 3:
		print(f"Using default includes: {DEFAULT_INCLUDES}")
		includes = DEFAULT_INCLUDES
	else:
		includes = []

	for i in range(2, len(sys.argv)):
		includes.append(sys.argv[i])

	result = []
	for include in includes:
		result.append("-include")
		result.append(include)
	return result


def run_preprocessor():
	arg_input = f"\n{MARKER}\n{sys.argv[1]}"
	arg_includes = get_includes()

	compiler_command = [CC, "-E", "-"]
	compiler_command.extend(arg_includes)
	try:
		return subprocess.check_output(
			compiler_command,
			input=str.encode(arg_input)
		).decode("UTF-8")
	except:
		print(f"\n{sys.argv[0]}: Error: Failed to run preprocessor.")
		sys.exit(1)


def clean_output(raw):
	stripped_marker = MARKER.strip()
	result = ""
	has_found_marker = False

	for line in iter(raw.splitlines()):
		if has_found_marker:
			result = result + line

		if line.strip() == stripped_marker:
			has_found_marker = True

	return result


def display_with_bat(cleaned):
	try:
		subprocess.run(
			["bat", "--language", "cpp"],
			input=str.encode(cleaned))
		return True
	except:
		return False


def main():
	if len(sys.argv) < 2:
		arg_error()

	preprocessor_output = run_preprocessor()
	cleaned = clean_output(preprocessor_output)
	if TRY_USE_BAT == False or display_with_bat(cleaned) == False:
		print(cleaned)
	sys.exit(0)


if __name__ == "__main__":
	main()
