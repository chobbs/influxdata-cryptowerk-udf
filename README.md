# Cryptowerk UDF Example

 Example in this directory implements a Cryptowerk verification request with the following specifications.

* Wants and provides a stream edge to Kapacitor.
* Verifies seals of previously registered hashes.

### Constructor

| Chaining Method | Description |
|:---------|:---------|
| **[blockchain]()** | Create a node that passes a retrievalId on crit Alert.  |

### Property Methods

| Setters | Description |
|:---|:---|
| **[retrievalId](#as)&nbsp;(&nbsp;`value`&nbsp;`string`)** | Option that specifies which hash to operate on..  |
| **[as](#as)&nbsp;(&nbsp;`value`&nbsp;`string`)** | The new name of the resulting state field.   |



### Review Chaining Methods
[Alert](https://docs.influxdata.com/kapacitor/v1.5/nodes/alert_node/), [Eval](https://docs.influxdata.com/kapacitor/v1.5/nodes/eval_node/), [Window](https://docs.influxdata.com/kapacitor/v1.5/nodes/window_node/), [Stream](https://docs.influxdata.com/kapacitor/v1.5/nodes/stream_node/), [InfluxDBOut](https://docs.influxdata.com/kapacitor/v1.5/nodes/influx_d_b_out_node/), .......: (DESCRIBE MORE)

### Description

Pass as stream point (At this moment only string fields will be able to be checked for blockchain.)

Example:


```javascript
    stream
        |from()
            .measurement('cryptowerk')
        |window()
            .period(1m)
            .every(1m)
        @blockchain()
            .retrievalId('retrievalId')
        |influxDBOut()
            .database('trusted-alerts')
            .retentionPolicy('autogen')
            .measurement('verified')
```

Note that as the first point in the given state has no previous point, its
state will be pressumed static and not passed through.
