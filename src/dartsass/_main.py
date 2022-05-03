import subprocess as sp
from ._options import *
from typing import Union
import os
import sys
import platform

__all__ = ["CompileError", "compile"]

_dirname = os.path.dirname(__file__)


def _machine():
    """Return type of machine."""
    if os.name == "nt" and sys.version_info[:2] < (2, 7):
        return os.environ.get(
            "PROCESSOR_ARCHITEW6432", os.environ.get("PROCESSOR_ARCHITECTURE", "")
        )
    else:
        return platform.machine()


def _os_bits(machine=_machine()):
    """Return bitness of operating system, or None if unknown."""
    machine2bits = {"AMD64": 64, "x86_64": 64, "i386": 32, "x86": 32}
    return machine2bits.get(machine, None)


_plat_sys = platform.system()
_plat_bits = _os_bits()

if _plat_sys == "Windows":
    if _plat_bits == 64:
        _dart_sass_path = os.path.join(
            _dirname, "./sass/windows-x64/dart-sass/sass.bat"
        )
    else:
        _dart_sass_path = os.path.join(
            _dirname, "./sass/windows-ia32/dart-sass/sass.bat"
        )
elif _plat_sys == "Darwin":
    if "ARM" in platform.uname().version:
        _dart_sass_path = os.path.join(_dirname, "./sass/macos-arm64/dart-sass/sass")
    else:
        _dart_sass_path = os.path.join(_dirname, "./sass/macos-x64/dart-sass/sass")
elif _plat_sys == "Linux":
    if _plat_bits == 64:
        if platform.machine() == "aarch64":  # Check if on ARM
            _dart_sass_path = os.path.join(
                _dirname, "./sass/linux-arm64/dart-sass/sass"
            )
        else:
            _dart_sass_path = os.path.join(_dirname, "./sass/linux-x64/dart-sass/sass")
    else:
        _dart_sass_path = os.path.join(_dirname, "./sass/linux-ia32/dart-sass/sass")


class CompileError(ValueError):
    pass


def compile(
    filenames: tuple[str, str] | str = None,
    dirnames: tuple[str, str] | str = None,
    string: tuple[str, str] | str = None,
    indented: bool = None,
    load_paths: list[str] = None,
    output_style: Union[OutputStyles.EXPANDED, OutputStyles.COMPRESSED] = None,
    charset: bool = None,
    error_css: bool = None,
    update: bool = False,
    source_map: Union[
        SourceMapOptions.NO_SOURCE_MAP,
        SourceMapOptions.SOURCE_MAP_URLS,
        SourceMapOptions.EMBED_SOURCES,
        SourceMapOptions.EMBED_SOURCE_MAP,
    ] = None,
    watch: bool = False,
    poll: bool = False,
    stop_on_error: bool = False,
) -> None | str:
    if list(map(bool, (filenames, dirnames, string))).count(True) != 1:
        raise ValueError(
            "Must specify exactly one of `filenames`, `dirnames`, or `string`"
        )
    extra_arguments = []
    if indented:
        extra_arguments.append(InputOutput.INDENTED)
    elif indented is False:
        extra_arguments.append(InputOutput.NO_INDENTED)
    if load_paths:
        for path in load_paths:
            extra_arguments.append(f"{InputOutput.LOAD_PATH}={path}")
    if output_style:
        extra_arguments.append(f"--style={output_style}")
    if charset:
        extra_arguments.append(InputOutput.CHARSET)
    elif charset is False:
        extra_arguments.append(InputOutput.NO_CHARSET)
    if error_css:
        extra_arguments.append(InputOutput.ERROR_CSS)
    elif error_css is False:
        extra_arguments.append(InputOutput.NO_ERROR_CSS)
    if update:
        extra_arguments.append(InputOutput.UPDATE)
    if source_map:
        extra_arguments.append(source_map)
    if watch:
        extra_arguments.append(OtherOptions.WATCH)
    if poll:
        if not watch:
            raise ValueError("`poll` requires `watch` to be enabled")
        extra_arguments.append(OtherOptions.POLL)
    if stop_on_error:
        extra_arguments.append(OtherOptions.STOP_ON_ERROR)

    return_val = None
    try:
        if type(dirnames) == str:
            p = sp.Popen(
                [_dart_sass_path, dirnames, *extra_arguments],
                stdout=sp.PIPE,
                stdin=sp.PIPE,
                stderr=sp.PIPE,
            )
        elif type(dirnames) == tuple:
            p = sp.check_output(
                [_dart_sass_path, ':'.join(dirnames), *extra_arguments],
                stdin=sp.PIPE,
                stderr=sp.PIPE,
            )
        elif type(filenames) == str:
            p = sp.Popen(
                [_dart_sass_path, filenames, *extra_arguments],
                stdout=sp.PIPE,
                stdin=sp.PIPE,
                stderr=sp.PIPE,
            )
            return_val = p.stdout.read().decode("utf-8")
        elif type(filenames) == tuple:
            p = sp.check_output(
                [_dart_sass_path, *filenames, *extra_arguments],
                stdin=sp.PIPE,
                stderr=sp.PIPE,
            )
        elif type(string) == str:
            p = sp.Popen(
                [_dart_sass_path, InputOutput.STDIN, *extra_arguments],
                stdout=sp.PIPE,
                stdin=sp.PIPE,
                stderr=sp.PIPE,
            )
            comm = p.communicate(string.encode("utf-8"))
            return_val = comm[0].decode("utf-8")
        elif type(string) == tuple:
            p = sp.Popen(
                [_dart_sass_path, InputOutput.STDIN, string[1], *extra_arguments],
                stdout=sp.PIPE,
                stdin=sp.PIPE,
                stderr=sp.PIPE,
            )
            comm = p.communicate(string[0].encode("utf-8"))
    except sp.CalledProcessError as e:
        raise CompileError(f"{e.returncode} - {e.output.decode('utf-8')}")
        
    return return_val
