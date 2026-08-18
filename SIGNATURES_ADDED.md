{
  "bomFormat": "CycloneDX",
  "specVersion": "1.6",
  "serialNumber": "urn:uuid:cf9295c6-4378-42ae-a73b-41592203c359",
  "version": 1,
  "metadata": {
    "timestamp": "2026-08-18T10:57:02.718643Z",
    "component": {
      "type": "application",
      "bom-ref": "application:third-party-source-components",
      "name": "third-party-source-components",
      "version": "1"
    }
  },
  "components": [
    {
      "type": "library",
      "bom-ref": "avro@1.12.1#avro_snif_libs",
      "name": "avro",
      "version": "1.12.1",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/apache/avro"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/apache/avro"
        },
        {
          "name": "source.ref",
          "value": "release-1.12.1"
        },
        {
          "name": "source.dir",
          "value": "avro_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/apache/avro@1.12.1",
      "cpe": "cpe:2.3:a:apache:avro:1.12.1:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "boost@1.85.0#boost_snif_libs",
      "name": "boost",
      "version": "1.85.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/boostorg/boost"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/boostorg/boost"
        },
        {
          "name": "source.ref",
          "value": "boost-1.85.0"
        },
        {
          "name": "source.dir",
          "value": "boost_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/boostorg/boost@1.85.0",
      "cpe": "cpe:2.3:a:boost:boost:1.85.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "brotli@1.1.0#brotli_snif_libs",
      "name": "brotli",
      "version": "1.1.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/google/brotli"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/google/brotli"
        },
        {
          "name": "source.ref",
          "value": "v1.1.0"
        },
        {
          "name": "source.dir",
          "value": "brotli_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/google/brotli@1.1.0",
      "cpe": "cpe:2.3:a:google:brotli:1.1.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "fmt@11.2.0#fmt_snif_libs",
      "name": "fmt",
      "version": "11.2.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/fmtlib/fmt"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/fmtlib/fmt"
        },
        {
          "name": "source.ref",
          "value": "11.2.0"
        },
        {
          "name": "source.dir",
          "value": "fmt_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/fmtlib/fmt@11.2.0",
      "cpe": "cpe:2.3:a:fmt:fmt:11.2.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "hyperscan@5.4.2#hyperscan_snif_libs",
      "name": "hyperscan",
      "version": "5.4.2",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/intel/hyperscan"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/intel/hyperscan"
        },
        {
          "name": "source.ref",
          "value": "v5.4.2"
        },
        {
          "name": "source.dir",
          "value": "hyperscan_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/intel/hyperscan@5.4.2",
      "cpe": "cpe:2.3:a:intel:hyperscan:5.4.2:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "jemalloc@5.1.0#jemalloc_snif_libs",
      "name": "jemalloc",
      "version": "5.1.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/jemalloc/jemalloc"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/jemalloc/jemalloc"
        },
        {
          "name": "source.ref",
          "value": "5.1.0"
        },
        {
          "name": "source.dir",
          "value": "jemalloc_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "inferred"
        }
      ],
      "purl": "pkg:github/jemalloc/jemalloc@5.1.0",
      "cpe": "cpe:2.3:a:jemalloc:jemalloc:5.1.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "libconfig@1.7.3#libconfig_snif_libs",
      "name": "libconfig",
      "version": "1.7.3",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/hyperrealm/libconfig"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/hyperrealm/libconfig"
        },
        {
          "name": "source.ref",
          "value": "v1.7.3"
        },
        {
          "name": "source.dir",
          "value": "libconfig_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "inferred"
        }
      ],
      "purl": "pkg:github/hyperrealm/libconfig@1.7.3",
      "cpe": "cpe:2.3:a:hyperrealm:libconfig:1.7.3:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "libxml2@2.14.4#libxml2_snif_libs",
      "name": "libxml2",
      "version": "2.14.4",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://gitlab.gnome.org/GNOME/libxml2"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://gitlab.gnome.org/GNOME/libxml2"
        },
        {
          "name": "source.ref",
          "value": "v2.14.4"
        },
        {
          "name": "source.dir",
          "value": "libxml2_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "cpe": "cpe:2.3:a:xmlsoft:libxml2:2.14.4:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "libzmq@4.3.5#libzmq_snif_libs",
      "name": "libzmq",
      "version": "4.3.5",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/zeromq/libzmq"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/zeromq/libzmq"
        },
        {
          "name": "source.ref",
          "value": "v4.3.5"
        },
        {
          "name": "source.dir",
          "value": "libzmq_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/zeromq/libzmq@4.3.5",
      "cpe": "cpe:2.3:a:zeromq:libzmq:4.3.5:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "lz4@1.10.0#lz4_snif_libs",
      "name": "lz4",
      "version": "1.10.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/lz4/lz4"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/lz4/lz4"
        },
        {
          "name": "source.ref",
          "value": "v1.10.0"
        },
        {
          "name": "source.dir",
          "value": "lz4_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/lz4/lz4@1.10.0",
      "cpe": "cpe:2.3:a:lz4_project:lz4:1.10.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "nghttp2@1.68.1#nghttp2_snif_libs",
      "name": "nghttp2",
      "version": "1.68.1",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/nghttp2/nghttp2"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/nghttp2/nghttp2"
        },
        {
          "name": "source.ref",
          "value": "v1.68.1"
        },
        {
          "name": "source.dir",
          "value": "nghttp2_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/nghttp2/nghttp2@1.68.1",
      "cpe": "cpe:2.3:a:nghttp2:nghttp2:1.68.1:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "oneTBB@2022.3.0#oneTBB_snif_libs",
      "name": "oneTBB",
      "version": "2022.3.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/uxlfoundation/oneTBB"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/uxlfoundation/oneTBB"
        },
        {
          "name": "source.ref",
          "value": "v2022.3.0"
        },
        {
          "name": "source.dir",
          "value": "oneTBB_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "inferred-family"
        }
      ],
      "purl": "pkg:github/uxlfoundation/oneTBB@2022.3.0",
      "cpe": "cpe:2.3:a:intel:threading_building_blocks:2022.3.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "openssl@3.5.5#openssl_snif_libs",
      "name": "openssl",
      "version": "3.5.5",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/openssl/openssl"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/openssl/openssl"
        },
        {
          "name": "source.ref",
          "value": "openssl-3.5.5"
        },
        {
          "name": "source.dir",
          "value": "openssl_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/openssl/openssl@3.5.5",
      "cpe": "cpe:2.3:a:openssl:openssl:3.5.5:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "rapidjson@1.1.0#rapidjson_snif_libs",
      "name": "rapidjson",
      "version": "1.1.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/Tencent/rapidjson"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/Tencent/rapidjson"
        },
        {
          "name": "source.ref",
          "value": "v1.1.0"
        },
        {
          "name": "source.dir",
          "value": "rapidjson_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/Tencent/rapidjson@1.1.0",
      "cpe": "cpe:2.3:a:tencent:rapidjson:1.1.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "re2@2023-03-01#re2_snif_libs",
      "name": "re2",
      "version": "2023-03-01",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/google/re2"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/google/re2"
        },
        {
          "name": "source.ref",
          "value": "2023-03-01"
        },
        {
          "name": "source.dir",
          "value": "re2_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "inferred"
        }
      ],
      "purl": "pkg:github/google/re2@2023-03-01",
      "cpe": "cpe:2.3:a:google:re2:2023-03-01:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "snappy@1.2.2#snappy_snif_libs",
      "name": "snappy",
      "version": "1.2.2",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/google/snappy"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/google/snappy"
        },
        {
          "name": "source.ref",
          "value": "1.2.2"
        },
        {
          "name": "source.dir",
          "value": "snappy_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/google/snappy@1.2.2",
      "cpe": "cpe:2.3:a:google:snappy:1.2.2:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "zlib@1.3.2#zlib_snif_libs",
      "name": "zlib",
      "version": "1.3.2",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/madler/zlib"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/madler/zlib"
        },
        {
          "name": "source.ref",
          "value": "v1.3.2"
        },
        {
          "name": "source.dir",
          "value": "zlib_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/madler/zlib@1.3.2",
      "cpe": "cpe:2.3:a:zlib:zlib:1.3.2:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "sqlite@3.50.4#sqlite_snif_libs",
      "name": "sqlite",
      "version": "3.50.4",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/sqlite/sqlite"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/sqlite/sqlite"
        },
        {
          "name": "source.ref",
          "value": "version-3.50.4"
        },
        {
          "name": "source.dir",
          "value": "sqlite_snif_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/sqlite/sqlite@3.50.4",
      "cpe": "cpe:2.3:a:sqlite:sqlite:3.50.4:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "libzmq@4.3.5#zeromq_agent_libs",
      "name": "libzmq",
      "version": "4.3.5",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/zeromq/libzmq"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/zeromq/libzmq"
        },
        {
          "name": "source.ref",
          "value": "v4.3.5"
        },
        {
          "name": "source.dir",
          "value": "zeromq_agent_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/zeromq/libzmq@4.3.5",
      "cpe": "cpe:2.3:a:zeromq:libzmq:4.3.5:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "poco@1.14.1#poco_agent_libs",
      "name": "poco",
      "version": "1.14.1",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/pocoproject/poco"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/pocoproject/poco"
        },
        {
          "name": "source.ref",
          "value": "poco-1.14.1-release"
        },
        {
          "name": "source.dir",
          "value": "poco_agent_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/pocoproject/poco@1.14.1",
      "cpe": "cpe:2.3:a:pocoproject:poco:1.14.1:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "libpcap@1.10.5#libpcap_agent_libs",
      "name": "libpcap",
      "version": "1.10.5",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/the-tcpdump-group/libpcap"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/the-tcpdump-group/libpcap"
        },
        {
          "name": "source.ref",
          "value": "libpcap-1.10.5"
        },
        {
          "name": "source.dir",
          "value": "libpcap_agent_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/the-tcpdump-group/libpcap@1.10.5",
      "cpe": "cpe:2.3:a:tcpdump:libpcap:1.10.5:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "libcgroup@3.1.0#libcgroup_agent_libs",
      "name": "libcgroup",
      "version": "3.1.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/libcgroup/libcgroup"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/libcgroup/libcgroup"
        },
        {
          "name": "source.ref",
          "value": "v3.1.0"
        },
        {
          "name": "source.dir",
          "value": "libcgroup_agent_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed-family"
        }
      ],
      "purl": "pkg:github/libcgroup/libcgroup@3.1.0",
      "cpe": "cpe:2.3:a:libcgroup_project:libcgroup:3.1.0:*:*:*:*:*:*:*"
    },
    {
      "type": "library",
      "bom-ref": "boost@1.86.0#boost_agent_libs",
      "name": "boost",
      "version": "1.86.0",
      "externalReferences": [
        {
          "type": "vcs",
          "url": "https://github.com/boostorg/boost"
        }
      ],
      "properties": [
        {
          "name": "source.repository",
          "value": "https://github.com/boostorg/boost"
        },
        {
          "name": "source.ref",
          "value": "boost-1.86.0"
        },
        {
          "name": "source.dir",
          "value": "boost_agent_libs"
        },
        {
          "name": "cpe.mapping.status",
          "value": "confirmed"
        }
      ],
      "purl": "pkg:github/boostorg/boost@1.86.0",
      "cpe": "cpe:2.3:a:boost:boost:1.86.0:*:*:*:*:*:*:*"
    }
  ],
  "dependencies": [
    {
      "ref": "application:third-party-source-components",
      "dependsOn": [
        "avro@1.12.1#avro_snif_libs",
        "boost@1.85.0#boost_snif_libs",
        "brotli@1.1.0#brotli_snif_libs",
        "fmt@11.2.0#fmt_snif_libs",
        "hyperscan@5.4.2#hyperscan_snif_libs",
        "jemalloc@5.1.0#jemalloc_snif_libs",
        "libconfig@1.7.3#libconfig_snif_libs",
        "libxml2@2.14.4#libxml2_snif_libs",
        "libzmq@4.3.5#libzmq_snif_libs",
        "lz4@1.10.0#lz4_snif_libs",
        "nghttp2@1.68.1#nghttp2_snif_libs",
        "oneTBB@2022.3.0#oneTBB_snif_libs",
        "openssl@3.5.5#openssl_snif_libs",
        "rapidjson@1.1.0#rapidjson_snif_libs",
        "re2@2023-03-01#re2_snif_libs",
        "snappy@1.2.2#snappy_snif_libs",
        "zlib@1.3.2#zlib_snif_libs",
        "sqlite@3.50.4#sqlite_snif_libs",
        "libzmq@4.3.5#zeromq_agent_libs",
        "poco@1.14.1#poco_agent_libs",
        "libpcap@1.10.5#libpcap_agent_libs",
        "libcgroup@3.1.0#libcgroup_agent_libs",
        "boost@1.86.0#boost_agent_libs"
      ]
    },
    {
      "ref": "avro@1.12.1#avro_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "boost@1.85.0#boost_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "brotli@1.1.0#brotli_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "fmt@11.2.0#fmt_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "hyperscan@5.4.2#hyperscan_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "jemalloc@5.1.0#jemalloc_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "libconfig@1.7.3#libconfig_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "libxml2@2.14.4#libxml2_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "libzmq@4.3.5#libzmq_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "lz4@1.10.0#lz4_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "nghttp2@1.68.1#nghttp2_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "oneTBB@2022.3.0#oneTBB_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "openssl@3.5.5#openssl_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "rapidjson@1.1.0#rapidjson_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "re2@2023-03-01#re2_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "snappy@1.2.2#snappy_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "zlib@1.3.2#zlib_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "sqlite@3.50.4#sqlite_snif_libs",
      "dependsOn": []
    },
    {
      "ref": "libzmq@4.3.5#zeromq_agent_libs",
      "dependsOn": []
    },
    {
      "ref": "poco@1.14.1#poco_agent_libs",
      "dependsOn": []
    },
    {
      "ref": "libpcap@1.10.5#libpcap_agent_libs",
      "dependsOn": []
    },
    {
      "ref": "libcgroup@3.1.0#libcgroup_agent_libs",
      "dependsOn": []
    },
    {
      "ref": "boost@1.86.0#boost_agent_libs",
      "dependsOn": []
    }
  ]
}
