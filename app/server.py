from starlette.applications import Starlette
from starlette.responses import HTMLResponse, JSONResponse
from starlette.staticfiles import StaticFiles
from starlette.middleware.cors import CORSMiddleware
import uvicorn, aiohttp, asyncio
from io import BytesIO

from fastai import *
from fastai.vision import *

# export_file_url = 'https://www.dropbox.com/s/v6cuuvddq73d1e0/export.pkl?raw=1'
export_file_url = 'https://www.dropbox.com/s/c2jbdqd6flm57ey/export.pkl?dl=0'
export_file_name = 'export.pkl'

#classes = ['black', 'grizzly', 'teddys']
classes = ['000_hatsune_miku', '001_kinomoto_sakura', '002_suzumiya_haruhi', '003_fate_testarossa', '004_takamachi_nanoha', '005_lelouch_lamperouge', '006_akiyama_mio', '007_nagato_yuki', '008_shana', '009_hakurei_reimu', '010_izumi_konata', '011_kirisame_marisa', '012_asahina_mikuru', '013_saber', '014_hiiragi_kagami', '015_c.c', '016_furukawa_nagisa', '017_louise', '018_kagamine_rin', '019_ayanami_rei', '020_remilia_scarlet', '021_hirasawa_yui', '022_kururugi_suzaku', '023_hiiragi_tsukasa', '024_fujibayashi_kyou', '025_souryuu_asuka_langley', '026_tohsaka_rin', '027_izayoi_sakuya', '028_tainaka_ritsu', '029_kallen_stadtfeld', '030_aisaka_taiga', '031_kotobuki_tsumugi', '032_yakumo_yukari', '033_kagamine_len', '034_sakagami_tomoyo', '035_yoko', '036_reisen_udongein_inaba', '037_lala_satalin_deviluke', '038_takara_miyuki', '039_yagami_hayate', '040_flandre_scarlet', '041_saigyouji_yuyuko', '042_tsukimura_mayu', '043_konpaku_youmu', '044_nakano_azusa', '045_patchouli_knowledge', '046_alice_margatroid', '047_sheryl_nome', '049_kyon', '050_megurine_luka', '051_houjou_reika', '052_ranka_lee', '053_kousaka_tamaki', '054_horo', '055_ibuki_fuuko', '056_nagi', '057_li_syaoran', '058_kochiya_sanae', '059_sairenji_haruna', '060_ichinose_kotomi', '061_furude_rika', '062_matou_sakura', '063_ryuuguu_rena', '064_amami_haruka', '065_sanzenin_nagi', '066_shameimaru_aya', '067_feena_fam_earthlight', '068_miyamura_miyako', '069_hayase_mitsuki', '070_nijihara_ink', '071_nagase_minato', '072_melon-chan', '073_subaru_nakajima', '074_daidouji_tomoyo', '075_katsura_hinagiku', '076_cirno', '077_yoshida_kazumi', '078_black_rock_shooter', '079_teana_lanster', '080_koizumi_itsuki', '081_yuzuhara_konomi', '083_shirou_kamui', '084_okazaki_tomoya', '085_sonozaki_mion', '086_tsuruya', '087_suzumiya_haruka', '088_vita', '089_shigure_asa', '090_minase_iori', '091_komaki_manaka', '092_shindou_kei', '093_yuuki_mikan', '094_fuyou_kaede', '095_nerine', '096_golden_darkness', '097_kamikita_komari', '098_mizunashi_akari', '100_houjou_satoko', '102_katagiri_yuuhi', '103_reinforce_zwei', '104_fukuzawa_yumi', '105_yuno', '106_nia', '107_chii', '111_suigintou', '112_hinamori_amu', '113_lisianthus', '114_natsume_rin', '116_pastel_ink', '118_noumi_kudryavka', '119_takatsuki_yayoi', '120_asakura_yume', '121_arcueid_brunestud', '123_midori', '125_sakai_yuuji', '127_setsuna_f_seiei', '129_primula', '131_belldandy', '132_minamoto_chizuru', '134_nunnally_lamperouge', '136_shirley_fenette', '137_sonsaku_hakufu', '138_kanu', '139_caro_ru_lushe', '140_seto_san', '143_miura_azusa', '144_kotegawa_yui', '146_shinku', '149_asakura_otome', '150_maria', '152_maka_albarn', '153_canal_volphied', '154_kobayakawa_yutaka', '155_vivio', '156_miyafuji_yoshika', '157_ogasawara_sachiko', '158_enma_ai', '159_andou_mahoro', '160_ayasaki_hayate', '161_ryougi_shiki', '164_shindou_chihiro', '165_rollo_lamperouge', '166_katsura_kotonoha', '168_asagiri_mai', '169_shihou_matsuri', '171_ikari_shinji', '172_kisaragi_chihaya', '173_reina', '174_hayama_mizuki', '175_saotome_alto', '176_sendou_erika', '178_milfeulle_sakuraba', '179_siesta', '180_matsuoka_miu', '181_allen_walker', '182_corticarte_apa_lagranges', '184_suzumiya_akane', '185_akihime_sumomo', '186_nanael', '188_aika_granzchesta', '189_akizuki_ritsuko', '190_kawashima_ami', '191_shidou_hikaru', '192_shirakawa_kotori', '193_kagurazaka_asuna', '195_erio_mondial', '196_kikuchi_makoto', '197_illyasviel_von_einzbern', '198_nogizaka_haruka', '199_kusugawa_sasara', '997_ana_coppola', '998_ito_nobue', '999_ito_chika']
path = Path(__file__).parent

app = Starlette()
app.add_middleware(CORSMiddleware, allow_origins=['*'], allow_headers=['X-Requested-With', 'Content-Type'])
app.mount('/static', StaticFiles(directory='app/static'))

async def download_file(url, dest):
    if dest.exists(): return
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            data = await response.read()
            with open(dest, 'wb') as f: f.write(data)

async def setup_learner():
    await download_file(export_file_url, path/export_file_name)
    try:
        learn = load_learner(path, export_file_name)
        return learn
    except RuntimeError as e:
        if len(e.args) > 0 and 'CPU-only machine' in e.args[0]:
            print(e)
            message = "\n\nThis model was trained with an old version of fastai and will not work in a CPU environment.\n\nPlease update the fastai library in your training environment and export your model again.\n\nSee instructions for 'Returning to work' at https://course.fast.ai."
            raise RuntimeError(message)
        else:
            raise

loop = asyncio.get_event_loop()
tasks = [asyncio.ensure_future(setup_learner())]
learn = loop.run_until_complete(asyncio.gather(*tasks))[0]
loop.close()

@app.route('/')
def index(request):
    html = path/'view'/'index.html'
    return HTMLResponse(html.open().read())

@app.route('/analyze', methods=['POST'])
async def analyze(request):
    data = await request.form()
    img_bytes = await (data['file'].read())
    img = open_image(BytesIO(img_bytes))
    prediction = learn.predict(img)[0]
    return JSONResponse({'result': str(prediction)})

if __name__ == '__main__':
    if 'serve' in sys.argv: uvicorn.run(app=app, host='0.0.0.0', port=5042)
