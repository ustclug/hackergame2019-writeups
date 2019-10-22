function Search-Dir {
	param (
		$Dir, $PathX, $PathY
	)
	if ($Dir.GetType().Name -eq "PathInfo") {
		$Path = $Dir
		$DirX = 0
		$DirY = 0
	} else {
		$Path = $Dir.PSPath
		$DirX = $Dir.X
		$DirY = $Dir.Y
		if ((Get-ChildItem $Path).Length -eq 1) {
			Write-Output ("EndPoint: (" + $DirX.ToString() + ", " + $DirY.ToString() + ")")
			return
		}
	}
	Get-ChildItem $Path | ForEach-Object {
		if (Confirm-Point $_ -PathX $PathX -PathY $PathY) {
		} elseif ($_.Flag) {
			Write-Output ("Flag: " + $_.Flag)
			exit 0
		} else {
			Search-Dir $_ -PathX ($PathX + $DirX) -PathY ($PathY + $DirY)
		}
	}
}

function Confirm-Point {
	param (
		$Point, $PathX, $PathY
	)
	for ($i = 0; $i -lt $PathX.Count; $i++) {
		if (($Point.X -eq $PathX[$i]) -and ($Point.Y -eq $PathY[$i])) {
			return $true
		}
	}
	return $false
}

Search-Dir $(Get-Location) @() @()