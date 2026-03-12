# -*- coding: utf-8 -*-

import os, sys, winsound, time, json
if __name__ == "__main__":
    BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
    if BASE_DIR not in sys.path:
        sys.path.insert(0, BASE_DIR)
import configuration  # Custom
from modules.capsys_mysql_command.capsys_mysql_command import (GenericDatabaseManager, DatabaseConfig) # Custom
from configuration import get_project_path

def get_info():
    return "Cette étape effectue le nettoyage et la fermeture des ressources en fin de test."

def run_step(log, config: configuration.AppConfig, update_percentage=lambda x: None):
    step_name = os.path.splitext(os.path.basename(__file__))[0]
    return_msg = {"step_name": step_name, "infos": []}
    # Ensure db is initialized
    if not hasattr(config, "db") or config.db is None:
        return_msg["infos"].append("Erreur : config.db n'est pas initialisé.")
        return 1, return_msg
    # We always save the name of the step in the db
    config.db.create("step_name", {"device_under_test_id": config.device_under_test_id, "step_name": step_name})
    success = 0

    # delete config.json file
    config_file_path = get_project_path("config.json")
    if os.path.exists(config_file_path):
        os.remove(config_file_path)
        log("Fichier config.json supprimé.", "blue")
    else:
        log("Problème lors de la suppression du fichier config.json.", "yellow")
        success = 2
        
    # Close serial port if open
    if hasattr(config, 'serDut') and config.serDut is not None and config.serDut.is_connected():
        try:
            config.serDut.close()
            log("Port série fermé.", "blue")
        except Exception as e:
            log(f"Erreur lors de la fermeture du port série : {e}", "yellow")
            success = 2

    # Close mcp23017
    if config.mcp_manager is None:
        success = 2
        log("Le MCP23017 n'avait pas été initialisé.", "yellow")
    else:
        for pin in configuration.MCP23017Pin:
            config.mcp_manager.digital_write(pin, False)
        log("Le MCP23017 a été réinitialisé.", "blue")
    
    # Close daq
    if config.daq_port == None or config.daq_manager == None:
        return 2, "Le DAQ n'avait pas été initialisé."
    else:
        pass

    # Beep PC
    for _ in range(3):
        winsound.Beep(1000, 200)  # 1000 Hz pendant 200 ms
        time.sleep(0.2)

    if success == 0:
        try:
            # Save into file config.weariness_threshold if it exists
            if hasattr(config, "weariness_threshold") and config.weariness_threshold is not None:
                weariness_file_path = configuration.USER_PATH_ROOT + config.configItems.bench_wear.path
                bench_wear_data = {}

                # Read existing JSON content to preserve other keys.
                if os.path.exists(weariness_file_path):
                    try:
                        with open(weariness_file_path, 'r', encoding='utf-8') as f:
                            loaded_data = json.load(f)
                            if isinstance(loaded_data, dict):
                                bench_wear_data = loaded_data
                    except Exception:
                        bench_wear_data = {}

                bench_wear_data[configuration.NAME_GUI] = config.weariness_threshold + 1

                with open(weariness_file_path, 'w', encoding='utf-8') as f:
                    json.dump(bench_wear_data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            log(f"Erreur lors de la mise à jour du fichier de seuils de banc de test : {e}", "yellow")
            success = 2
        return_msg["infos"].append("Nettoyage effectué avec succès.")
        return success, return_msg
    elif success == 2:
        return_msg["infos"].append("Nettoyage effectué partiellement.")
        return success, return_msg
    else:
        return_msg["infos"].append("Erreur inconnue lors du nettoyage.")
        return 1, return_msg

if __name__ == "__main__":
    """Allow to run this script directly for testing purposes."""

    def log_message(message, color):
        print(f"{color}: {message}")

    # Initialize config
    config = configuration.AppConfig()
    config.arg.show_all_logs = False
    config.arg.product_list_id = configuration.PRODUCT_LIST_ID_DEFAULT

    # Initialize Database
    config.db_config = DatabaseConfig(password="root")
    config.db = GenericDatabaseManager(config.db_config, debug=False)
    config.db.connect()
    
    # Launch the initialisation step
    from steps.s01.initialisation import run_step as run_step_init
    success_end, message_end = run_step_init(log_message, config)
    print(message_end)
    
    # Launch this step
    success, message = run_step(log_message, config)
    print(message)