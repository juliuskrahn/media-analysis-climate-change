is_about_climate_change_sql_statement = {
    "en":
        """
        ((title ~* 'climat' AND title ~* '(chang|catastroph|disaster|transform|adjust|trend|warm|heat|cool|variab|chill|
        politic|project|target|goal|conference|protect|effect|harm|damage|impact|contract|law|mission|demonstrat|protest
        |activis|plan|resolution|decision|strategy)')
        OR (title ~* '(global|earth|world|international|hemisphere)' 
            AND (
                title ~* '(warm|heat|cool|chill)'
                OR (title ~* 'temperature' AND title ~* '(increas|rising|rise|decreas)')
            )
        )
        OR (title ~* 'greenhouse' AND title ~* '(gas|effect|emission)'))
        """,
    "de":
        """
        ((title ~* 'klima' AND title ~* '(wandel|änder|wechsel|krise|erwärm|warm|kält|kalt|erhitz|problem|zustand|
        politik|desaster|schwank|projekt|schutz|schädlich|schadet|schaden|auswirk|ziel|plan|gipfel|treffen|vertrag|
        ausschuss|beschluss|strategie|aktivis|demo|einsatz|einsetz|streik|katastroph|trend|gesetz)')
        OR (title ~* '(global|erde|welt|international)'
            AND (
                title ~* '(wärm|erhitz|hitze|heiz|warm|temperatur)'
                OR (title ~* 'temperatur' AND title ~* '(steig|stieg|senk|sink|sank)')
            )
        )
        OR (title ~* 'treibhaus' AND title ~* '(gas|effekt|emission)'))
        """,
}
