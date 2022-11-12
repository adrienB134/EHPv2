import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st


@st.cache()
def load_data(_uploadedFile):
    ehp_data = pd.read_csv(_uploadedFile, sep=";", skiprows=16)
    st.write(ehp_data)

    ehp_data = pd.DataFrame(ehp_data)
    ehp_data = ehp_data.rename(columns={"Horodatage": "index"}).set_index(
        "index", drop=False
    )
    ehp_data = ehp_data.iloc[::10, :]
    return ehp_data


def rcp(ehp_data, app_mode):
    df = ehp_data[["EHP001MP", "EHP002MP"]]
    fig = px.line(
        df,
        title="Evolution de la pression RCP pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)


def pression_refoulement_mule(ehp_data, app_mode):
    df = ehp_data[["EHP003MP"]]
    df = pd.DataFrame(df)
    df = df.assign(Pression_limite_EHP003MP_236bars=236)
    df = df.assign(Seuil_d_arrêt_RCV191PO_232bars=232)
    df = df.assign(Seuil_d_alarme_haute_pression_refoulement_RCV191PO_228bars=228)
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe RCV191PO",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)
    st.write(df)


def pression_refoulement_mule_detail(ehp_data, app_mode):
    df = ehp_data["EHP003MP"] > 4
    positions = np.flatnonzero(df)
    df = ehp_data["EHP003MP"].iloc[positions]
    df = pd.DataFrame(df)
    df = df.assign(Pression_limite_EHP003MP_236bars=236)
    df = df.assign(Seuil_d_arrêt_RCV191PO_232bars=232)
    df = df.assign(Seuil_d_alarme_haute_pression_refoulement_RCV191PO_228bars=228)
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe RCV191PO pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "Pression_limite_EHP003MP_236bars": "Pression limite EHP003MP 236bars",
        "Seuil_d_arrêt_RCV191PO_232bars": "Seuil d'arrêt RCV191PO 232bars",
        "Seuil_d_alarme_haute_pression_refoulement_RCV191PO_228bars": "Seuil d'alarme haute pression refoulement \nRCV191PO 228bars",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))

    st.write(fig)


def temperature_gros_composants_fond_de_cuve(ehp_data, app_mode):
    df = ehp_data[["EHP001MT", "EHP002MT", "EHP003MT"]]
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe RCV191PO pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)


def temperature_gros_composants_couvercle_et_pressu(ehp_data, app_mode):
    df = ehp_data[["EHP004MT", "EHP005MT", "EHP006MT"]]
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe RCV191PO pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "EHP004MT": "EHP004MT - Bride de cuve",
        "EHP005MT": "EHP005MT - Bride de couvercle",
        "EHP006MT": "EHP006MT - JEP Pressu",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
    st.write(fig)


def temperature_gros_composants_gv(ehp_data, app_mode):
    if app_mode == "900":
        df = ehp_data[["EHP007MT", "EHP008MT", "EHP009MT"]]
        fig = px.line(
            df,
            title="Evolution de la pression de refoulement de la pompe RCV191PO pendant l'épreuve",
            labels={
                "index": "Date",
                "value": "Pression (bar)",
                "variable": "Valeurs",
            },
        )
        st.write(df)
        value_map = {
            "EHP007MT": "EHP007MT - GV1",
            "EHP008MT": "EHP008MT - GV2",
            "EHP009MT": "EHP009MT - GV3",
        }
        fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
        st.write(fig)

    if app_mode == "1300":
        df = ehp_data[["EHP007MT", "EHP008MT", "EHP009MT", "EHP010MT"]]
        fig = px.line(
            df,
            title="Evolution de la pression de refoulement de la pompe RCV191PO pendant l'épreuve",
            labels={
                "index": "Date",
                "value": "Pression (bar)",
                "variable": "Valeurs",
            },
        )
        value_map = {
            "EHP007MT": "EHP007MT - GV1",
            "EHP008MT": "EHP008MT - GV2",
            "EHP009MT": "EHP009MT - GV3",
            "EHP010MT": "EHP010MT - GV4",
        }
        fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))
        st.write(fig)


def pgrad(ehp_data, app_mode):
    df = ehp_data[["EHP001MPGrad", "EHP002MPGrad"]]
    df = df.assign(val_max_grad=4)
    df = df.assign(val_min_grad=-4)
    fig = px.line(
        df,
        title="Gradients de Pression de l'EHP",
        labels={
            "index": "Date",
            "value": "Gradient de Pression (bar/min)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "val_max_grad": "Valeur Max Gradient (+4 bar/min)",
        "val_min_grad": "Valeur Min Gradient (-4 bar/min)",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))

    st.write(fig)


def tmoy(ehp_data, app_mode):
    df = ehp_data[["TMOY"]]
    fig = px.line(
        df,
        title="Suivi de la Tmoy de l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)


def tgrad(ehp_data, app_mode):
    if app_mode == "900":
        container = st.container()
        Tmoy50 = st.select_slider(label=" date Tmoy>50°C", options=ehp_data.index)
        Tmoy51 = st.select_slider(label=" date Tmoy<50°C", options=ehp_data.index)

        with st.expander("Paramètres de limites"):
            TmoySup1 = st.number_input(label="Tmoy supérieure à froid", value=14)
            TmoySup2 = st.number_input(label="Tmoy supérieure à chaud", value=28)
            TmoyInf1 = st.number_input(label="Tmoy inférieure à froid", value=-14)
            TmoyInf2 = st.number_input(label="Tmoy inférieure à chaud", value=-28)

        df = ehp_data[["TGRAD"]]
        df2 = df.assign(Tmoymin=-14)
        df2 = df2.assign(Tmoymax=14)
        df2.loc[df2.index <= Tmoy50, "Tmoymax"] = TmoySup1
        df2.loc[df2.index > Tmoy50, "Tmoymax"] = TmoySup2
        df2.loc[df2.index > Tmoy51, "Tmoymax"] = TmoySup1
        df2.loc[df2.index <= Tmoy50, "Tmoymin"] = TmoyInf1
        df2.loc[df2.index > Tmoy50, "Tmoymin"] = TmoyInf2
        df2.loc[df2.index > Tmoy51, "Tmoymin"] = TmoyInf1

        fig_rcp = px.line(
            df2,
            title="Suivi du gradient de Tmoy de l'EHP",
            labels={
                "index": "Date",
                "value": "Température (°C/h)",
                "variable": "Valeurs",
            },
        )
        container.write(fig_rcp)
    else:
        st.write("Erreur")


def tfluid1(ehp_data, app_mode):
    df = ehp_data[["RCP009MT", "RCP010MT", "RCP028MT"]]
    fig = px.line(
        df,
        title="Suivi des températures fluide pendant l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)


def tfluid2(ehp_data, app_mode):
    df = ehp_data[["RCP029MT", "RCP043MT", "RCP044MT"]]
    fig = px.line(
        df,
        title="Suivi des températures fluide pendant l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)


def tfluid3(ehp_data, app_mode):
    df = ehp_data[["RCP055MT", "RCP056MT", "RCP400MT", "RCP404MT"]]
    fig = px.line(
        df,
        title="Suivi des températures fluide pendant l'EHP",
        labels={
            "index": "Date",
            "value": "Température (°C)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)


def tmetal1(ehp_data, app_mode):
    df = ehp_data[["EHP001MTGrad", "EHP002MTGrad", "EHP003MTGrad"]]
    fig = px.line(
        df,
        title="Gradient des températures métal pendant l'EHP - Fond de cuve",
        labels={
            "index": "Date",
            "value": "Température (°C/h)",
            "variable": "Valeurs",
        },
    )
    st.write(fig)


def tmetal2(ehp_data, app_mode):
    df = ehp_data[["EHP004MTGrad", "EHP005MTGrad", "EHP006MTGrad"]]
    fig = px.line(
        df,
        title="Gradient des températures métal pendant l'EHP - Couvercle et Pressu",
        labels={
            "index": "Date",
            "value": "Température (°C/h)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "EHP004MTGrad": "EHP004MTGrad - Bride de cuve",
        "EHP005MTGrad": "EHP005MTGrad - Bride de couvercle",
        "EHP006MTGrad": "EHP006MTGrad - JEP Pressu",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))

    st.write(fig)


def tmetal3(ehp_data, app_mode):
    df = ehp_data[["EHP007MTGrad", "EHP008MTGrad", "EHP009MTGrad", "EHP010MTGrad"]]
    fig = px.line(
        df,
        title="Gradient des températures métal pendant l'EHP - GV",
        labels={
            "index": "Date",
            "value": "Température (°C/h)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "EHP007MTGrad": "EHP007MTGrad - GV1",
        "EHP008MTGrad": "EHP008MTGrad - GV2",
        "EHP009MTGrad": "EHP009MTGrad - GV3",
        "EHP010MTGrad": "EHP010MTGrad - GV4",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))

    st.write(fig)


def evolution_pression_epreuve(ehp_data, app_mode):
    df = ehp_data[["EHP001MP"]] > 172
    positions = np.flatnonzero(df)
    df = ehp_data[["EHP001MP"]].iloc[positions]
    df2 = ehp_data[["EHP002MP"]] > 172
    positions = np.flatnonzero(df2)
    df2 = ehp_data[["EHP002MP"]].iloc[positions]
    df = pd.concat([df, df2])
    df = df.assign(pression_max=207.8)
    df = df.assign(pression_min=206.9)
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe RCV191PO pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "pression_max": "207,8 bar",
        "pression_min": "206,9 bar",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))

    st.write(fig)


def evolution_pression_epreuve_palier(ehp_data, app_mode):
    df = ehp_data[["EHP001MP"]] > 205
    positions = np.flatnonzero(df)
    df = ehp_data[["EHP001MP"]].iloc[positions]
    df2 = ehp_data[["EHP002MP"]] > 205
    positions = np.flatnonzero(df2)
    df2 = ehp_data[["EHP002MP"]].iloc[positions]
    df = pd.concat([df, df2])
    df = df.assign(pression_max=206.9)
    df = df.assign(pression_min=206)
    fig = px.line(
        df,
        title="Evolution de la pression de refoulement de la pompe RCV191PO pendant l'épreuve",
        labels={
            "index": "Date",
            "value": "Pression (bar)",
            "variable": "Valeurs",
        },
    )
    value_map = {
        "pression_max": "206,9 bar",
        "pression_min": "206 bar",
    }
    fig.for_each_trace(lambda t: t.update(name=value_map.get(t.name, t.name)))

    st.write(fig)


def about():
    st.write("Réalisé par Adrien Berthélémé")
    st.write("adrien.bertheleme@gmail.com")
    st.write("06.72.65.24.97")
    st.write("Code source dispo ici: https://github.com/adrienB134/EHPv2")
    st.button("Retour", on_click=st.empty)


def main():
    UploadedFile = st.sidebar.file_uploader(
        label="Charger le fichier de dépouillement."
    )
    container_sidebar = st.sidebar.container()

    if st.sidebar.button("A propos"):
        about()
        st.stop()

    if UploadedFile is None:
        st.warning(
            "Charger le fichier de dépouillement. Si erreur vérifier que la ligne commençant par 'horodatage' est bien en ligne 17 dans le .csv"
        )
        st.stop()
    elif UploadedFile is not None:
        app_mode = container_sidebar.selectbox("Palier", ["900", "1300"])
        courbe = container_sidebar.selectbox(
            "courbe",
            [
                "Evolution de la pression RCP pendant l'épreuve",
                "Evolution de la pression de refoulement de la pompe RCV191PO",
                "Evolution de la pression de refoulement de la pompe RCV191PO - détail",
                "Température des gros composants du CPP - Fond de cuve",
                "Température des gros composants du CPP - couvercle et pressu",
                "Température des gros composants du CPP - GVs",
                "Gradients de Pression de l'EHP",
                "Suivi de la Tmoy de l'EHP",
                "Suivi du gradient de Tmoy de l'EHP",
                "Suivi des températures fluide pendant l'EHP - 1",
                "Suivi des températures fluide pendant l'EHP - 2",
                "Suivi des températures fluide pendant l'EHP - 3",
                "Gradient des températures métal pendant l'EHP - Fond de cuve",
                "Gradient des températures métal pendant l'EHP - Couvercle et Pressu",
                "Gradient des températures métal pendant l'EHP - GV",
                "Evolution de la pression pendant le palier d'épreuve",
                "Evolution de la pression pendant le palier d'épreuve - détail",
            ],
        )

        chart_data = load_data(UploadedFile)
        st.info(
            "Mettre la courbe en plein écran avant d'enregistrer en utilisant le bouton appareil photo",
            icon="⚠️",
        )

        if courbe == "Evolution de la pression RCP pendant l'épreuve":
            rcp(chart_data, app_mode)
        if courbe == "Evolution de la pression de refoulement de la pompe RCV191PO":
            pression_refoulement_mule(chart_data, app_mode)
        if (
            courbe
            == "Evolution de la pression de refoulement de la pompe RCV191PO - détail"
        ):
            pression_refoulement_mule_detail(chart_data, app_mode)
        if courbe == "Température des gros composants du CPP - Fond de cuve":
            temperature_gros_composants_fond_de_cuve(chart_data, app_mode)
        if courbe == "Température des gros composants du CPP - couvercle et pressu":
            temperature_gros_composants_couvercle_et_pressu(chart_data, app_mode)
        if courbe == "Température des gros composants du CPP - GVs":
            temperature_gros_composants_gv(chart_data, app_mode)
        if courbe == "Gradients de Pression de l'EHP":
            pgrad(chart_data, app_mode)
        if courbe == "Suivi de la Tmoy de l'EHP":
            tmoy(chart_data, app_mode)
        if courbe == "Suivi du gradient de Tmoy de l'EHP":
            tgrad(chart_data, app_mode)
        if courbe == "Suivi des températures fluide pendant l'EHP - 1":
            tfluid1(chart_data, app_mode)
        if courbe == "Suivi des températures fluide pendant l'EHP - 2":
            tfluid2(chart_data, app_mode)
        if courbe == "Suivi des températures fluide pendant l'EHP - 3":
            tfluid3(chart_data, app_mode)
        if courbe == "Gradient des températures métal pendant l'EHP - Fond de cuve":
            tmetal1(chart_data, app_mode)
        if (
            courbe
            == "Gradient des températures métal pendant l'EHP - Couvercle et Pressu"
        ):
            tmetal2(chart_data, app_mode)
        if courbe == "Gradient des températures métal pendant l'EHP - GV":
            tmetal3(chart_data, app_mode)
        if courbe == "Evolution de la pression pendant le palier d'épreuve":
            evolution_pression_epreuve(chart_data, app_mode)
        if courbe == "Evolution de la pression pendant le palier d'épreuve - détail":
            evolution_pression_epreuve_palier(chart_data, app_mode)


if __name__ == "__main__":
    main()
