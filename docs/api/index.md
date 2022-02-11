Module dechainy_web
===================

Functions
---------

    
`index() ‑> str`
:   Rest endpoint to test whether the server is correctly working
    
    Returns:
        str: The default message string

    
`manage_plugin(plugin_name: str = None) ‑> Union[module, List[module]]`
:   Rest endpoint to get, create or modify an instance of a given Plugin
    
    Args:
        plugin_name (str): The name of the Plugin
        probe_name (str): The name of the instance
    
    Returns:
        Union[ProbeConfig, str]: The instance if GET, else its name

    
`manage_probe(plugin_name: str = None, probe_name: str = None) ‑> dechainy.plugins.Probe`
:   Rest endpoint to get, create or modify an instance of a given Plugin
    
    Args:
        plugin_name (str): The name of the Plugin
        probe_name (str): The name of the instance
    
    Returns:
        Union[ProbeConfig, str]: The instance if GET, else its name

    
`retrieve_metric(plugin_name: str, probe_name: str, program_type: str, metric_name: str = None) ‑> <built-in function any>`
:   Rest endpoint to retrieve the value of a defined metric
    
    Args:
        plugin_name (str): The name of the plugin
        probe_name (str): The name of the Adaptmon instance
        program_type (str): The type of the program (Ingress/Egress)
        metric_name (str): The name of the metric to be retrieved
    
    Returns:
        any: The value of the metric