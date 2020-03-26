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
       |     ^                     |
     (R/W)   '-------.             |
       |             |             |
Event Generator    State           |
       ^         (Optional)        |
       |                           |
       '---------------------------'
```

Config File Explained
---------------------

You may define the I/O pattern to be simulated here, as well as all the
tunables.

__Schema__

TODO: fill me once it is stable, and in the mood :)

__Example__

```javascript
{
  /* some metadata of the simulation run */
  "output-prefix": "factory-ceph",

  /* defines sources of latencies */
  "sources": [
    {
      "name": "nvme-ssd-read",
      "type": "normal-distribution",
      "parameters": {   // defined per `type`
        "mu": 2000.0,
        "sigma": 128.0
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
    {
      "name": "read",
      "type": "event",
      "probability": 0.8,   // uniform scale, may not adds up to exactly 1
      "workflow": [
        // ...
      ]
    },

    // you get the idea...
  ],
}
```

Modular Design
--------------

```text
EventLoop

EventGenerator

LatencySource
  '-- ConstantSource
  '-- SamplingSource
  |     '-- NormalDistributionSource
  |     '-- UniformDistributionSource
  '-- StochasticProcessSource

PerfCounter
```

#### Simulated Event Loop

The event loop ticks by _events_ rather than _time_.

It  would  be  easier to translate stochastic model into config files,  however,
making it less intuitive to acquire time-related numbers, like through-put.

For every tick, the event loop takes one event from the event generator.

This   effectively  limits  the  range  of  models  the  tool  can  simulate  to
_single-threaded serial_ events.  However,  certain synchronized parallel events
can  be  modeled with operators like `maximum`,  where the lengthiest process of
the batch dominates the section.

#### Event Generator

Generates an event every tick.  For example, for modeling I/O latency, events to
be generated could be read events, write events, promotion events and so on. The
framework  assumes that every events associates to some latency  (defined in the
`sources`  section  in  the  config file),  otherwise we won't need to model the
event since it doesn't contribute to the final output number.

#### Performance Counter

Sample some output numbers from event loop, and store them in some counters.

Source Tree Organization
------------------------

```text
src/
  '-- config/
  |     '-- __init__.py
  '-- evloop/
  '-- evgen/
  |     '-- __init__.py
  |     '-- event_generator.py
  |     '-- latency_sources/
  |           '-- __init__.py
  |           '-- latency_source.py
  |           '-- constant_sources.py
  |           '-- sampling_sources.py
  '-- perfcounter/
  '-- test/                         // run with `python -m unittest test/xxx.py`
```