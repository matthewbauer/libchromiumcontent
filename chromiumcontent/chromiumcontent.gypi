{
  'variables': {
    # Enalbe using proprietary codecs.
    'proprietary_codecs': 1,
    'ffmpeg_branding': 'Chrome',
    # And the gold's flags are not available in system's ld neither.
    'linux_use_gold_flags': 0,
    # Make Linux build contain debug symbols, this flag will add '-g' to cflags.
    'linux_dump_symbols': 1,
    # The Linux build of libchromiumcontent.so depends on, but doesn't
    # provide, tcmalloc by default.  Disabling tcmalloc here also prevents
    # any conflicts when linking to binaries or libraries that don't use
    # tcmalloc.
    'linux_use_tcmalloc': 0,
    # Using libc++ requires building for >= 10.7.
    'mac_deployment_target': '10.8',
    # The 10.8 SDK does not work well with C++11.
    'mac_sdk_min': '10.9',
    # Use OpenSSL.
    'use_openssl': 1,
    # Use the standard way of linking with msvc runtime.
    'win_use_allocator_shim': 0,
    'win_release_RuntimeLibrary': '2',
    # The V8 libraries.
    'v8_libraries': '["v8", "v8_snapshot", "v8_nosnapshot", "v8_external_snapshot", "v8_base", "v8_libbase", "v8_libplatform"]',
    # The icu libraries.
    'icu_libraries': '["icui18n", "icuuc"]',
    'conditions': [
      ['OS=="win"', {
        # On Chrome 41 this is disabled on Windows.
        'v8_use_external_startup_data': 1,
      }],
      ['OS=="linux"', {
        # Enable high DPI support on Linux.
        'enable_hidpi': 1,
        # Use Dbus.
        'use_dbus': 1,
      }],
      ['OS=="linux" and host_arch=="ia32"', {
        # Use system installed clang for building.
        'make_clang_dir': '/usr',
        'clang': 1,
        'clang_use_chrome_plugins': 0,
      }],
    ],
  },
  'target_defaults': {
    'msvs_disabled_warnings': [
        # class 'std::xx' needs to have dll-interface. Chrome turns this off
        # for component builds, and we need to too.
        4251,
        # The file contains a character that cannot be represented in these
        # current code page
        4819,
        # no matching operator delete found; memory will not be freed if
        # initialization throws an exception
        4291,
        # non dll-interface class used as base for dll-interface class
        4275,
        # 'GetVersionExW': was declared deprecated
        4996,
    ],
    'xcode_settings': {
      'WARNING_CFLAGS': [
        '-Wno-deprecated-declarations',
      ],
      # Use C++11 library.
      'CLANG_CXX_LIBRARY': 'libc++',  # -stdlib=libc++
    },
    # Force exporting icu's symbols.
    'defines': [
      'U_COMBINED_IMPLEMENTATION',
      # Defining "U_COMBINED_IMPLEMENTATION" will add "explicit" for some
      # constructors, make sure it doesn' happen.
      'UNISTR_FROM_CHAR_EXPLICIT=',
      'UNISTR_FROM_STRING_EXPLICIT=',
      'U_NO_DEFAULT_INCLUDE_UTF_HEADERS=0',
    ],
    'defines!': [
      'U_STATIC_IMPLEMENTATION',
    ],
    'conditions': [
      ['OS=="linux" and host_arch=="ia32"', {
        'cflags!': [
          # Clang 3.4 doesn't support these flags.
          '-Wno-absolute-value',
          '-Wno-inconsistent-missing-override',
          '-Wno-pointer-bool-conversion',
          '-Wno-tautological-pointer-compare',
          '-Wno-unused-local-typedef',
          '-Wno-undefined-bool-conversion',
          '-Wno-tautological-undefined-compare',
        ],
      }],
    ],
    'target_conditions': [
      ['_type=="static_library" and OS=="linux" and component=="static_library"', {
        'standalone_static_library': 1,
      }],
      ['_target_name in <(v8_libraries) + <(icu_libraries)', {
        'xcode_settings': {
          'DEAD_CODE_STRIPPING': 'NO',  # -Wl,-dead_strip
          'GCC_INLINES_ARE_PRIVATE_EXTERN': 'NO',
          'GCC_SYMBOLS_PRIVATE_EXTERN': 'NO',
        },
        'cflags!': [
          '-fvisibility=hidden',
          '-fdata-sections',
          '-ffunction-sections',
        ],
        'cflags_cc!': ['-fvisibility-inlines-hidden'],
      }],
      ['_target_name in <(v8_libraries) + ["mksnapshot"]', {
        'defines': [
          'V8_SHARED',
          'BUILDING_V8_SHARED',
        ],
        # Override src/v8/build/toolchain.gypi's RuntimeLibrary setting.
        'configurations': {
          'Release': {
            'msvs_settings': {
              'VCCLCompilerTool': {
                'RuntimeLibrary': '<(win_release_RuntimeLibrary)',
              },
            },
          },
        },
      }],
      ['_target_name=="gtk2ui"', {
        'type': 'static_library',
        'standalone_static_library': 1,
        'cflags': [
          '-Wno-sentinel',
        ],
      }],
    ],
  },
}
