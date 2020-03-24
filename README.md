latency-sim
===========

Random tool for my college graduation design.


Basic Design
============

Intuition and Guidelines
------------------------

* __Configuration File Based__ for better flexibility
* __Function Oriented__ for better code
* __Performance Counter Included__ for more statistics

```text
      Perf Counter <-.
                     |
       .--> Simulated Event Loop --.
       |                           |
     (R/W)                         |
       |                           |
Event Generator                    |
       ^                           |
       |                           |
       '---------------------------'
```

Config File Explained
---------------------

You may define the I/O pattern to be simulated here, as well as all the
tunables.

__Schema__

TODO

__Example__

```javascript
{
  /* some metadata of the simulation run */
  "output-prefix": "factory-ceph",

  /* defines sources of latencies */
  "sources": [
    {
      "name": "nvme-ssd-read",
      "sample-operation": {
        "type": "normal-distribution",
        "parameters": {   // defined per `type`
          "mu": 2000.0,
          "sigma": 128.0
        }
      }
    },

    // ...
  ],

  /* defines numbers to monitor and collect (every step) */
  "collectibles": [
    /***********************************************************
                                   .-- nvme-sdd-write
                                  /
    cache-promote_single-write add
                                  \
                                   '-- network-communication
     ***********************************************************/
    {
      "name": "cache-promote_single-write",
      "type": "intermediate",   // may indicate postprocessing to perform

      /* defines how the final output figure (of every step) is generated,
         item "$" in the list will be the output. */
      "workflow": [
        {
          "symbol": "$",
          "type": "calculate",
          "operator": "addition",   // or "+"
          "operands": [
            {
              "source": "network-communication"   // symbol defined in `sources`
              // may define additional "parameters" field to overwrite those
              // previously defined in `sources` section
            },
            {
              "source": "nvme-ssd-write"
            }
          ]
        }
      ]
    },

    /***********************************************************
                      .-- hdd-read
                     /
    cache-promote add                          .-- (replica-1) ...
                     \                        /
                      '-- (write-to-cache) max --- (replica-2) ...
                                              \
                                               '-- (replica-3) ...
     ***********************************************************/
    {
      "name": "cache-promote",
      "type": "intermediate",
      "workflow": [
        {
          "symbol": "replicate-1",
          "type": "sample",
          "source": "cache-promote_single-write"  // symbol defined previously
        },
        {
          "symbol": "replicate-2",
          "type": "sample",
          "source": "cache-promote_single-write"
        },
        {
          "symbol": "replicate-3",
          "type": "sample",
          "source": "cache-promote_single-write"
        },
        {
          "symbol": "write-to-cache",
          "type": "calculate",
          "operator": "maximum",
          "operands": [
            {
              "source": "replica-1",
            },
            {
              "source": "replica-2",
            },
            {
              "source": "replica-3",
            }
          ]
        },
        {
          "symbol": "$",
          "type": "calculate",
          "operator": "addition",
          "operands": [
            {
              "source": "hdd-read",
            },
            {
              "source": "write-to-cache",
            }
          ]
        }
      ]
    },

    // you get the idea...
  ],
}
```

Modular Design
--------------

#### Simulated Event Loop

#### Event Generator

#### Performance Counter

Source Tree Organization
------------------------