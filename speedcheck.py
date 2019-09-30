import requests
import json
import sys
import time
import os

api_key = sys.argv[1]

locations = {
    "NY": {
        "cities": ["Boston", "New York"],
        "country": "US",
        "testCnt": 50,
        "urls": {
            "ttfb": {
                "m247-rp1-nyc": "https://1-1381-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000",
                "wz-rp2-us5": "https://1-1017-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000"
            },

            "ping": {
                "m247-rp1-nyc": "1-1381-19-9.b.cdn13.com",
                "wz-rp2-us5": "1-1017-19-9.b.cdn13.com"
            },

            "trace": {
                "m247-rp1-nyc": "1-1381-19-9.b.cdn13.com",
                "wz-rp2-us5": "1-1017-19-9.b.cdn13.com"
            }
        }
    },

    "MIA": {
        "cities": ["Miami", "Fort Lauderdale"],
        "country": "US",
        "testCnt": 50,
        "urls": {
            "ttfb": {
                "m247-rp1-mia": "https://1-1383-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000",
                "wz-rp52-us0": "https://1-329-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000"
            },

            "ping": {
                "m247-rp1-mia": "1-1383-19-9.b.cdn13.com",
                "wz-rp52-us0": "1-329-19-9.b.cdn13.com"
            },

            "trace": {
                "m247-rp1-mia": "1-1383-19-9.b.cdn13.com",
                "wz-rp52-us0": "1-329-19-9.b.cdn13.com"
            },
        }
    },

    "SPA": {
        "cities": [],
        "country": "ES",
        "testCnt": 100,
        "urls": {
            "ttfb": {
                "m247-rp1-spa": "https://1-1382-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000",
                "wz-rp79-nl0": "https://1-958-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000"
            },
            "ping": {
                "m247-rp1-spa": "1-1382-19-9.b.cdn13.com",
                "wz-rp79-nl0": "1-958-19-9.b.cdn13.com"
            },
            "trace": {
                "m247-rp1-spa": "1-1382-19-9.b.cdn13.com",
                "wz-rp79-nl0": "1-958-19-9.b.cdn13.com"
            }
        }
    },

    "PT": {
        "cities": [],
        "country": "PT",
        "testCnt": 100,
        "urls": {
            "ttfb": {
                "m247-rp1-spa": "https://1-1382-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000",
                "wz-rp79-nl0": "https://1-958-19-9.b.cdn13.com/hls/001/468/434/240p.h264.mp4/seg-44-v1-a1.ts?cdn_hash=f7243df8d0169dfe794dd81008895430&cdn_creation_time=1569581376&cdn_ttl=4320000"
            },
            "ping": {
                "m247-rp1-spa": "1-1382-19-9.b.cdn13.com",
                "wz-rp79-nl0": "1-958-19-9.b.cdn13.com"
            },
            "trace": {
                "m247-rp1-spa": "1-1382-19-9.b.cdn13.com",
                "wz-rp79-nl0": "1-958-19-9.b.cdn13.com"
            }
        }
    }
}

testtypes = {
    "ttfb": {
        "body": json.loads(
            '''{
            "testSettings": {
              "Method": "GET",
              "MaxBytes": 524288,
              "Timeout": 5000,
              "TestCount": 100,
              "Sources": [ ],
              "Destinations": [],
              "ProbeInfoProperties": [
                "IPAddress",
                "Latitude",
                "Longitude",
                "ProbeID",
                "CountryCode",
                "CityName",
                "DNSResolver",
                "ConnectionType",
                "Platform",
                "ASN",
                "Network"
              ]
            }
            }'''
        ),
        "start_url": "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/StartHttpTest?apikey={}",
        "result_url": "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/GetHttpResults?apikey={}&testID={}"
    },

    "ping": {
        "body": json.loads(
            '''{
              "testSettings": {
                "PingType": "icmp",
                "BufferSize": 32,
                "Count": 3,
                "Fragment": 1,
                "Ipv4only": 0,
                "Ipv6only": 0,
                "Resolve":    0,
                "Sleep": 1000,
                "Ttl":    128,
                "Timeout":    1000,
                "TestCount": 100,
                "Sources":    [],
                "Destinations": [],
                "ProbeInfoProperties":    [
                  "Latitude",
                  "Longitude",
                  "ProbeID",
                  "IPAddress",
                  "ASN",
                  "CountryCode",
                  "CityName"
                ]
              }
            }'''
        ),
        "start_url": "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/StartPingTest?apikey={}",
        "result_url": "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/GetPingResults?apikey={}&testID={}"
    },

    "trace": {
        "body": json.loads(
            '''{
              "testSettings": {
                  "BufferSize": 32,
                      "Count": 3,
                      "Fragment": 1,
                      "Ipv4only": 0,
                      "Ipv6only": 0,
                      "MaxFailedHops": 0,
                      "Resolve": 1,
                      "Sleep": 300,
                      "Ttl": 128,
                      "TtlStart": 1,
                      "Timeout": 600000,
                      "HopTimeout": 1000,
                      "TestCount": 10,
                      "Sources": [],
                      "Destinations": [],
                      "ProbeInfoProperties": [
                        "Latitude",
                        "Longitude",
                        "ProbeID",
                        "CountryCode",
                        "CityName"
                      ]
              }
            }'''
        ),
        "start_url": "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/StartTracertTest?apikey={}",
        "result_url": "https://kong.speedcheckerapi.com:8443/ProbeAPIv2/GetTracertResults?apikey={}&testID={}"
    }
}


TOTAL_REQS = 0
for name, location in locations.items():
    for testtype, destinations in location['urls'].items():

        if testtype not in sys.argv[2:]:
            continue

        body = testtypes[testtype]['body']
        u1 = testtypes[testtype]['start_url']
        u2 = testtypes[testtype]['result_url']
        for tag, destination in destinations.items():
            body['testSettings']['Sources'] = [{"CountryCode": location['country']}]
            body['testSettings']['TestCount'] = location['testCnt']

            if len(location['cities']):
                body['testSettings']['Sources'] = [{"CountryCode": location['country'], "CityName": city} for city in location['cities']]

            body['testSettings']['Destinations'] = [destination]

            now = time.gmtime()
            destdir = "results_{}/".format(time.strftime('%Y-%m-%d_%H', now))

            if not os.path.isdir(destdir):
                os.makedirs(destdir)

            fname_prefix = "{}{}_{}_to_{}.{}".format(destdir, time.strftime('%Y-%m-%d-%H-%M-%S', now), name, tag, testtype)
            infile = fname_prefix + ".req"
            outfile = fname_prefix + ".json"

            r = requests.post(u1.format(api_key), json=body)
            TOTAL_REQS += 1

            resultid = None
            if r.status_code == 200:
                resp = r.json()
                for tname, params in resp.items():
                    resultid = params['TestID']
            else:
                print("ERR: {} {}".format(r.status_code, r.text))

            with open(infile, 'w') as f:
                f.write("POST: {}\n".format(u1.format(api_key)))
                f.write("GET: curl -o {} '{}'\n".format(outfile, u2.format(api_key, resultid)))
                f.write("STATUS: {}\n".format(r.status_code))
                f.write("BODY:\n")
                f.write(json.dumps(body, indent=True) + "\n")
                f.write("RESP: {}\n".format(r.text))

print("Total api calls: {}".format(TOTAL_REQS))
