# Türkçe kısa kullanım

Yedi skill, seçilen araçların üzerine özgün ve kanıta dayalı iş akışları ekler. Paket araçları kurmaz, erişim anahtarı sağlamaz ve gerçek entegrasyonları otomatik çalıştırmaz.

| İhtiyaç | Skill |
| --- | --- |
| Ajan araç sırası/argüman regresyonu | `agent-trajectory-regression` |
| Tenant izolasyonu ve RLS rol matrisi | `postgres-tenant-isolation` |
| OpenAPI uç durumları ve sözleşme hataları | `openapi-contract-probes` |
| Ajan/RAG izlerinde gecikme ve hata analizi | `trace-failure-diagnosis` |
| İzinli, maskelenmiş oturumdan SOP çıkarma | `masked-session-to-sop` |
| Kaynaklı sentetik test verisi ve sızıntı kontrolü | `grounded-synthetic-datasets` |
| PDF tablosunda sayfa/koordinat kanıtı | `pdf-table-evidence` |

Önce ilgili `SKILL.md`, `references/example.md` ve `assets/case.json` dosyalarını okuyun. [Kurulum rehberindeki](INSTALLATION.md) doğru alana seçtiğiniz skill klasörünü bütünüyle kopyalayın; varsa aynı adlı dosyaları incelemeden değiştirmeyin.

Claude Code'da `/trace-failure-diagnosis`, Codex CLI/IDE'de `$trace-failure-diagnosis` ile görev verebilirsiniz. Örnek: “Bu sentetik span'lerde örtüşen süreleri iki kez saymadan gecikmeyi hesapla; eksik kanıtı belirt.”

Yerel kontroller:

```sh
python3 scripts/validate_package.py
python3 scripts/check_fixture.py
python3 -m unittest discover -s tests -v
```

Bunlar model veya gerçek araç testleri değildir. [Değerlendirme planı](EVALUATION.md) gerçek Claude/Codex oturumlarını ayrı ölçer. Gerçek host değerlendirmeleri ve upstream entegrasyonları henüz yapılmadı.

Örnekler tamamen sentetiktir. Gerçek müşteri verisi, anahtar, kişisel dosya, üretim veritabanı veya izinsiz oturum kaydı kullanmayın. Özgün içerik MIT lisanslıdır; upstream lisans bildirimleri kendi koşullarını korur.
