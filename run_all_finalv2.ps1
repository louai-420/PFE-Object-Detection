# Script PowerShell — Tester toutes les vidéos avec le pipeline v2
# Sortie : outputs/finalv2_<nom_video>/

$MODEL = "outputs/models/gas_flare_yolo11m_v1/weights/best.pt"
$PYTHON = ".venv\Scripts\python"
$CONF = 0.4

$videos = @(
    "data/watermarked_preview.mp4",
    "data/Flare stack short#unwanted gas fire off#short.mp4",
    "data/Gas flaring in action.mp4",
    "data/gettyimages-2166244461-640_adpp.mp4",
    "data/gettyimages-2161543143-640_adpp.mp4",
    "data/istockphoto-825730420-640_adpp_is.mp4",
    "data/FDownloader.net-2172847936361652-(1080p).mp4",
    "data/IMG_1638.mov",
    "data/IMG_1639.mov",
    "data/IMG_4386.mov",
    "data/163282211-flare-stacks-oil-refinery-are-.mp4",
    "data/268255879-oil-well-tall-natural-gas-flar.mp4",
    "data/test_flare.mp4",
    "data/test_flare_real.mp4",
    "data/istockphoto-1292015596-640_adpp_is.mp4",
    "data/istockphoto-1156375950-640_adpp_is.mp4",
    "data/istockphoto-1459909866-640_adpp_is.mp4"
)

$total = $videos.Count
$idx = 0

foreach ($video in $videos) {
    $idx++
    # Extraire le nom de base sans extension
    $basename = [System.IO.Path]::GetFileNameWithoutExtension($video)
    $outdir = "outputs/finalv2_$basename"

    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host " [$idx/$total] $basename" -ForegroundColor Cyan
    Write-Host "   Source : $video" -ForegroundColor Gray
    Write-Host "   Output : $outdir" -ForegroundColor Gray
    Write-Host "========================================" -ForegroundColor Cyan

    & $PYTHON src/realtime_monitor.py --source $video --model $MODEL --conf $CONF --output $outdir

    if ($LASTEXITCODE -ne 0) {
        Write-Host "  [ERREUR] Echec sur $basename" -ForegroundColor Red
    } else {
        Write-Host "  [OK] $basename termine" -ForegroundColor Green
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Green
Write-Host " TOUTES LES VIDEOS ONT ETE TRAITEES ($total/$total)" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Green
