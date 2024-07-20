# coding: utf-8
##############################################################################
#
# Author: Hector Ivan Valencia Muñoz
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/> LGPLv3.
#
# View UML Secuence Diagram: Copy code of flow_chart.puml file in 
# https://www.planttext.com/
#
##############################################################################

from robocorp.tasks import task
from robocorp import browser
from RPA.Tables import Tables

table = Tables()

@task
def validate_nit():
    """Consult the RUT status on the DIAN website for a list of NITs provided in a CSV file
    and save the results in a new CSV file."""
    # Set the browser wait time
    browser.configure(slowmo=200,)
    
    # Open URL
    open_website()
    
    # Validate NITs
    validate_records()

def open_website():
    """Open URL"""
    browser.goto("https://muisca.dian.gov.co/WebRutMuisca/DefConsultaEstadoRUT.faces")

def validate_on_website(nit):
    """Query the DIAN website and return the results."""
    xpath_nit = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:numNit"]'
    xpath_search = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:btnBuscar"]'
    xpath_dv = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:dv"]'
    xpath_apl1 = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerApellido"]'
    xpath_apl2 = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:segundoApellido"]'
    xpath_nom1 = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:primerNombre"]'
    xpath_nom2 = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:otrosNombres"]'
    xpath_raz = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:razonSocial"]'
    xpath_status = '//*[@id="vistaConsultaEstadoRUT:formConsultaEstadoRUT:estado"]'
    
    page = browser.page()
    page.fill(xpath_nit, nit)
    page.click(xpath_search)  

    if page.query_selector(xpath_apl1):
        result_query_web = {
            "nid": nit,
            "dv": page.query_selector(xpath_dv).inner_text(),
            "apl1": page.query_selector(xpath_apl1).inner_text(),
            "apl2": page.query_selector(xpath_apl2).inner_text(),
            "nom1": page.query_selector(xpath_nom1).inner_text(),
            "nom2": page.query_selector(xpath_nom2).inner_text(),
            "raz": "",
            "estado": page.query_selector(xpath_status).inner_text()
        }
    elif page.query_selector(xpath_raz):
        result_query_web = {
            "nid": nit,
            "dv": page.query_selector(xpath_dv).inner_text(),
            "apl1": "",
            "apl2": "",
            "nom1": "",
            "nom2": "",
            "raz": page.query_selector(xpath_raz).inner_text(),
            "estado": page.query_selector(xpath_status).inner_text()
        }
    else:
        result_query_web = {
            "nid": nit,
            "dv": "",
            "apl1": "",
            "apl2": "",
            "nom1": "",
            "nom2": "",
            "raz": "",
            "estado": "NO SE ENCUENTRA EN RUT"
        }
    return result_query_web

def validate_records():
    """Validate NIT records and save results."""
    csv_columns = ["nid", "dv", "apl1", "apl2", "nom1", "nom2", "raz", "estado"]
    nit_validar = table.read_table_from_csv("nid_validar.csv", header=True, columns=["nid", "dv"])
    nit_validados = table.read_table_from_csv("nid_validados.csv", header=True, columns=csv_columns)
    nit_validar_result = table.create_table(columns=csv_columns)

    # Create a set of validated NITs for faster lookup
    nit_validados_set = set(row["nid"] for row in nit_validados)

    for nit_row in nit_validar:
        nit = nit_row["nid"]
        if nit in nit_validados_set:
            for nit_val_row in nit_validados:
                if nit == nit_val_row["nid"]:
                    table.add_table_row(nit_validar_result, nit_val_row)
                    break
        else:
            result_query_web = validate_on_website(nit)
            table.add_table_row(nit_validar_result, result_query_web)
            if result_query_web["estado"] != "NO SE ENCUENTRA EN RUT":
                table.add_table_row(nit_validados, result_query_web)  

    table.write_table_to_csv(nit_validar_result, path="nid_validar_result.csv", header=True)
    table.write_table_to_csv(nit_validados, path="nid_validados.csv", header=True)

    return nit_validar_result
