
df_comparison = """SELECT l.unique_id AS unique_id_l,
       r.unique_id AS unique_id_r,
       l.source_dataset AS source_dataset_l,
       r.source_dataset AS source_dataset_r,
       l.surname_std AS surname_std_l,
       r.surname_std AS surname_std_r,
       l.forename1_std AS forename1_std_l,
       r.forename1_std AS forename1_std_r,
       l.forename2_std AS forename2_std_l,
       r.forename2_std AS forename2_std_r,
       l.forename3_std AS forename3_std_l,
       r.forename3_std AS forename3_std_r,
       l.forename4_std AS forename4_std_l,
       r.forename4_std AS forename4_std_r,
       l.forename5_std AS forename5_std_l,
       r.forename5_std AS forename5_std_r,
       l.dob_std AS dob_std_l,
       r.dob_std AS dob_std_r,
       l.pnc_number_std AS pnc_number_std_l,
       r.pnc_number_std AS pnc_number_std_r,
       '0' AS match_key
FROM df AS l
CROSS JOIN df AS r
WHERE concat(l.source_dataset, '-__-', l.unique_id) < concat(r.source_dataset, '-__-', r.unique_id)
AND l.source_dataset != r.source_dataset"""

df_with_gamma = """SELECT source_dataset_l,
       unique_id_l,
       source_dataset_r,
       unique_id_r,
       surname_std_l,
       surname_std_r,
       forename1_std_l,
       forename1_std_r,
       forename2_std_l,
       forename2_std_r,
       forename3_std_l,
       forename3_std_r,
       forename4_std_l,
       forename4_std_r,
       forename5_std_l,
       forename5_std_r,
       CASE
           WHEN surname_std_l IS NULL
                OR surname_std_r IS NULL THEN -1
           WHEN jaro_winkler_sim(surname_std_l, surname_std_r) >= 1.0 THEN 3
           WHEN (jaro_winkler_sim(ifnull(surname_std_l, '1234abcd5678'), ifnull(forename1_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(surname_std_l, '1234abcd5678'), ifnull(forename2_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(surname_std_l, '1234abcd5678'), ifnull(forename3_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(surname_std_l, '1234abcd5678'), ifnull(forename4_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(surname_std_l, '1234abcd5678'), ifnull(forename5_std_r, '987pqrxyz654')) >= 1.0) THEN 2
           WHEN Dmetaphone(surname_std_l) = Dmetaphone(surname_std_r) THEN 1
           WHEN Dmetaphone(surname_std_l) = Dmetaphone(surname_std_r) THEN 1
           WHEN jaro_winkler_sim(surname_std_l, surname_std_r) >= 0.88 THEN 1
           ELSE 0
       END AS gamma_surname_std,
       CASE
           WHEN forename1_std_l IS NULL
                OR forename1_std_r IS NULL THEN -1
           WHEN jaro_winkler_sim(forename1_std_l, forename1_std_r) >= 1.0 THEN 3
           WHEN (jaro_winkler_sim(ifnull(forename1_std_l, '1234abcd5678'), ifnull(surname_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename1_std_l, '1234abcd5678'), ifnull(forename2_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename1_std_l, '1234abcd5678'), ifnull(forename3_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename1_std_l, '1234abcd5678'), ifnull(forename4_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename1_std_l, '1234abcd5678'), ifnull(forename5_std_r, '987pqrxyz654')) >= 1.0) THEN 2
           WHEN Dmetaphone(forename1_std_l) = Dmetaphone(forename1_std_r) THEN 1
           WHEN Dmetaphone(forename1_std_l) = Dmetaphone(forename1_std_r) THEN 1
           WHEN jaro_winkler_sim(forename1_std_l, forename1_std_r) >= 0.88 THEN 1
           ELSE 0
       END AS gamma_forename1_std,
       CASE
           WHEN forename2_std_l IS NULL
                OR forename2_std_r IS NULL THEN -1
           WHEN jaro_winkler_sim(forename2_std_l, forename2_std_r) >= 1.0 THEN 3
           WHEN (jaro_winkler_sim(ifnull(forename2_std_l, '1234abcd5678'), ifnull(surname_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename2_std_l, '1234abcd5678'), ifnull(forename1_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename2_std_l, '1234abcd5678'), ifnull(forename3_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename2_std_l, '1234abcd5678'), ifnull(forename4_std_r, '987pqrxyz654')) >= 1.0
                 OR jaro_winkler_sim(ifnull(forename2_std_l, '1234abcd5678'), ifnull(forename5_std_r, '987pqrxyz654')) >= 1.0) THEN 2
           WHEN Dmetaphone(forename2_std_l) = Dmetaphone(forename2_std_r) THEN 1
           WHEN Dmetaphone(forename2_std_l) = Dmetaphone(forename2_std_r) THEN 1
           WHEN jaro_winkler_sim(forename2_std_l, forename2_std_r) >= 0.88 THEN 1
           ELSE 0
       END AS gamma_forename2_std,
       CASE
           WHEN forename3_std_l IS NULL
                OR forename3_std_r IS NULL THEN -1
           WHEN forename3_std_l = forename3_std_r THEN 1
           ELSE 0
       END AS gamma_forename3_std,
       dob_std_l,
       dob_std_r,
       CASE
           WHEN (dob_std_l IS NULL
                 OR dob_std_r IS NULL) THEN -1
           WHEN dob_std_l = dob_std_r
                AND substr(dob_std_l, -5) = '01-01' THEN 4
           WHEN dob_std_l = dob_std_r THEN 5
           WHEN levenshtein(dob_std_l, dob_std_r) <= 1 THEN 3
           WHEN abs(datediff(dob_std_l, dob_std_r)) <= 365 THEN 2
           WHEN abs(datediff(dob_std_l, dob_std_r)) <= 10*365 THEN 1
           ELSE 0
       END AS gamma_dob_std,
       pnc_number_std_l,
       pnc_number_std_r,
       CASE
           WHEN pnc_number_std_l IS NULL
                OR pnc_number_std_r IS NULL THEN -1
           WHEN pnc_number_std_l = pnc_number_std_r THEN 2
           WHEN levenshtein(pnc_number_std_l, pnc_number_std_r) <= 0 THEN 2
           WHEN levenshtein(pnc_number_std_l, pnc_number_std_r) <= 2 THEN 1
           ELSE 0
       END AS gamma_pnc_number_std
FROM df_comparison"""

df_with_gamma_probs = """SELECT source_dataset_l,
       unique_id_l,
       source_dataset_r,
       unique_id_r,
       surname_std_l,
       surname_std_r,
       forename1_std_l,
       forename1_std_r,
       forename2_std_l,
       forename2_std_r,
       forename3_std_l,
       forename3_std_r,
       forename4_std_l,
       forename4_std_r,
       forename5_std_l,
       forename5_std_r,
       gamma_surname_std,
       CASE
           WHEN gamma_surname_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_surname_std = 0 THEN cast(0.99725548973543565178800918147317134 AS DOUBLE)
           WHEN gamma_surname_std = 1 THEN cast(0.00159537137977009985806420289122798 AS DOUBLE)
           WHEN gamma_surname_std = 2 THEN cast(0.00033013987809683370761373866208999 AS DOUBLE)
           WHEN gamma_surname_std = 3 THEN cast(0.00081899900669745676756727803535796 AS DOUBLE)
       END AS prob_gamma_surname_std_non_match,
       CASE
           WHEN gamma_surname_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_surname_std = 0 THEN cast(0.04649045112467044271742366845501238 AS DOUBLE)
           WHEN gamma_surname_std = 1 THEN cast(0.04139301328538667196221823019186559 AS DOUBLE)
           WHEN gamma_surname_std = 2 THEN cast(0.00786904121689270888428957562155119 AS DOUBLE)
           WHEN gamma_surname_std = 3 THEN cast(0.90424749437305018684440938159241341 AS DOUBLE)
       END AS prob_gamma_surname_std_match,
       gamma_forename1_std,
       CASE
           WHEN gamma_forename1_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_forename1_std = 0 THEN cast(0.98723766613504415623481236252700910 AS DOUBLE)
           WHEN gamma_forename1_std = 1 THEN cast(0.00434970797804014493170843280722693 AS DOUBLE)
           WHEN gamma_forename1_std = 2 THEN cast(0.00272077268345129229601409015515401 AS DOUBLE)
           WHEN gamma_forename1_std = 3 THEN cast(0.00569185320346440263433729356279400 AS DOUBLE)
       END AS prob_gamma_forename1_std_non_match,
       CASE
           WHEN gamma_forename1_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_forename1_std = 0 THEN cast(0.04244583561609208827158923327260709 AS DOUBLE)
           WHEN gamma_forename1_std = 1 THEN cast(0.05722777918198598823273925972898724 AS DOUBLE)
           WHEN gamma_forename1_std = 2 THEN cast(0.01063373415504790218955033509473651 AS DOUBLE)
           WHEN gamma_forename1_std = 3 THEN cast(0.88969265104687400569360988811240532 AS DOUBLE)
       END AS prob_gamma_forename1_std_match,
       gamma_forename2_std,
       CASE
           WHEN gamma_forename2_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_forename2_std = 0 THEN cast(0.96813125410065403730897060086135752 AS DOUBLE)
           WHEN gamma_forename2_std = 1 THEN cast(0.00899249790135536221369338960585083 AS DOUBLE)
           WHEN gamma_forename2_std = 2 THEN cast(0.00945283761618772103152430474892753 AS DOUBLE)
           WHEN gamma_forename2_std = 3 THEN cast(0.01342341038180283781244828134049385 AS DOUBLE)
       END AS prob_gamma_forename2_std_non_match,
       CASE
           WHEN gamma_forename2_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_forename2_std = 0 THEN cast(0.06616037999984493434002530420912080 AS DOUBLE)
           WHEN gamma_forename2_std = 1 THEN cast(0.03891377945042830827082624978174863 AS DOUBLE)
           WHEN gamma_forename2_std = 2 THEN cast(0.02156295920635845075885583810304524 AS DOUBLE)
           WHEN gamma_forename2_std = 3 THEN cast(0.87336288134336836908033774307114072 AS DOUBLE)
       END AS prob_gamma_forename2_std_match,
       gamma_forename3_std,
       CASE
           WHEN gamma_forename3_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_forename3_std = 0 THEN cast(0.99403453706420108471064622790436260 AS DOUBLE)
           WHEN gamma_forename3_std = 1 THEN cast(0.00596546293579895605535545755060411 AS DOUBLE)
       END AS prob_gamma_forename3_std_non_match,
       CASE
           WHEN gamma_forename3_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_forename3_std = 0 THEN cast(0.12278441817288233972593758380753570 AS DOUBLE)
           WHEN gamma_forename3_std = 1 THEN cast(0.87721558182711767415185022400692105 AS DOUBLE)
       END AS prob_gamma_forename3_std_match,
       dob_std_l,
       dob_std_r,
       gamma_dob_std,
       CASE
           WHEN gamma_dob_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_dob_std = 0 THEN cast(0.56809978365876356853902962029678747 AS DOUBLE)
           WHEN gamma_dob_std = 1 THEN cast(0.38462640947393622603556195826968178 AS DOUBLE)
           WHEN gamma_dob_std = 2 THEN cast(0.04534027248271822047032131308696989 AS DOUBLE)
           WHEN gamma_dob_std = 3 THEN cast(0.00187004818921093643804831607724282 AS DOUBLE)
           WHEN gamma_dob_std = 4 THEN cast(0.00000090762805663393017550476943311 AS DOUBLE)
           WHEN gamma_dob_std = 5 THEN cast(0.00006257856731443046873104851801628 AS DOUBLE)
       END AS prob_gamma_dob_std_non_match,
       CASE
           WHEN gamma_dob_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_dob_std = 0 THEN cast(0.00536174093558949502180688284624921 AS DOUBLE)
           WHEN gamma_dob_std = 1 THEN cast(0.01470084970026688982180917975028933 AS DOUBLE)
           WHEN gamma_dob_std = 2 THEN cast(0.01619763948575476605884482239616773 AS DOUBLE)
           WHEN gamma_dob_std = 3 THEN cast(0.04794441530614954039002384433842963 AS DOUBLE)
           WHEN gamma_dob_std = 4 THEN cast(0.00415231962753553982686804957324966 AS DOUBLE)
           WHEN gamma_dob_std = 5 THEN cast(0.91164303494470377842162633896805346 AS DOUBLE)
       END AS prob_gamma_dob_std_match,
       pnc_number_std_l,
       pnc_number_std_r,
       gamma_pnc_number_std,
       CASE
           WHEN gamma_pnc_number_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_pnc_number_std = 0 THEN cast(0.99999317458539882519374941693968140 AS DOUBLE)
           WHEN gamma_pnc_number_std = 1 THEN cast(0.00000670017763197660070793263559219 AS DOUBLE)
           WHEN gamma_pnc_number_std = 2 THEN cast(0.00000012523696933365013432288680856 AS DOUBLE)
       END AS prob_gamma_pnc_number_std_non_match,
       CASE
           WHEN gamma_pnc_number_std = -1 THEN cast(1 AS DOUBLE)
           WHEN gamma_pnc_number_std = 0 THEN cast(0.01890714511824432078612723273636220 AS DOUBLE)
           WHEN gamma_pnc_number_std = 1 THEN cast(0.00689753912703955536500632916840914 AS DOUBLE)
           WHEN gamma_pnc_number_std = 2 THEN cast(0.97419531575471618456418809728347696 AS DOUBLE)
       END AS prob_gamma_pnc_number_std_match
FROM df_with_gamma"""


df_e = """SELECT (cast(1.876373054439382e-07 AS DOUBLE) * prob_gamma_surname_std_match * prob_gamma_forename1_std_match * prob_gamma_forename2_std_match * prob_gamma_forename3_std_match * prob_gamma_dob_std_match * prob_gamma_pnc_number_std_match)/((cast(1.876373054439382e-07 AS DOUBLE) * prob_gamma_surname_std_match * prob_gamma_forename1_std_match * prob_gamma_forename2_std_match * prob_gamma_forename3_std_match * prob_gamma_dob_std_match * prob_gamma_pnc_number_std_match) + (cast(0.9999998123626945 AS DOUBLE) * prob_gamma_surname_std_non_match * prob_gamma_forename1_std_non_match * prob_gamma_forename2_std_non_match * prob_gamma_forename3_std_non_match * prob_gamma_dob_std_non_match * prob_gamma_pnc_number_std_non_match)) AS match_probability,
       source_dataset_l,
       unique_id_l,
       source_dataset_r,
       unique_id_r,
       surname_std_l,
       surname_std_r,
       forename1_std_l,
       forename1_std_r,
       forename2_std_l,
       forename2_std_r,
       forename3_std_l,
       forename3_std_r,
       forename4_std_l,
       forename4_std_r,
       forename5_std_l,
       forename5_std_r,
       gamma_surname_std,
       gamma_forename1_std,
       gamma_forename2_std,
       gamma_forename3_std,
       dob_std_l,
       dob_std_r,
       gamma_dob_std,
       pnc_number_std_l,
       pnc_number_std_r,
       gamma_pnc_number_std
FROM df_with_gamma_probs"""
