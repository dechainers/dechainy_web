# Reference guide

This section covers most of the basic operations provided by the web functionality.
Apart from the healthy check route `/`, HTTP routes can be grouped in the following categories:

1. [Plugins Routes](#plugins-routes)
2. [Probes Routes](#probes-routes)
3. [Probes Metrics Routes](#probes-metrics-routes)

## Plugins Routes

* `/plugins` methods=['GET', 'POST', 'PUT', 'DELETE']: used to manage all plugins, or create/patch a specific one provided in the request body.
* `/plugins/<plugin_name>` methods=['DELETE']: used to delete a specific plugin.

## Probes Routes

* `/probes` methods=['GET', 'DELETE']: used to manage all probes of all plugins.
* `/probes/<plugin_name>` methods=['GET', 'POST', 'DELETE']: used to manage all probes of a specific plugin, or create a new one provided in the request body.
* `/probes/<plugin_name>/<probe_name>` methods=['GET', 'DELETE']: used to manage a specific probe of a given plugin.

## Probes Metrics Routes

* `/probes/<plugin_name>/<probe_name>/<program_type>/metrics` methods=['GET']: used to return all the metrics defined within the eBPF code of the probe.
`/probes/<plugin_name>/<probe_name>/<program_type>/metrics/<metric_name>` methods=['GET']: used to return a specific metric defined in the eBPF code of the probe.
