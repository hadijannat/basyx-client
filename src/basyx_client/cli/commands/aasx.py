"""AASX package commands."""

from __future__ import annotations

from pathlib import Path
from typing import Optional

import typer

from basyx_client.cli.config import get_client_from_context
from basyx_client.cli.output import (
    console,
    format_output,
    print_error,
    print_success,
    print_verbose,
)

app = typer.Typer(help="AASX package operations")


def _extract_package_summary(pkg: dict) -> dict[str, str]:
    """Extract summary from an AASX package info."""
    return {
        "package_id": pkg.get("packageId", ""),
        "aas_ids": ", ".join(pkg.get("aasIds", []))[:50],
    }


@app.command("list")
def list_packages(
    ctx: typer.Context,
    limit: int = typer.Option(100, "--limit", "-l", help="Maximum number of results"),
    cursor: Optional[str] = typer.Option(None, "--cursor", "-c", help="Pagination cursor"),
    aas_id: Optional[str] = typer.Option(None, "--aas-id", help="Filter by AAS ID"),
    all_pages: bool = typer.Option(False, "--all", "-a", help="Fetch all pages"),
) -> None:
    """List all AASX packages."""
    print_verbose(ctx, "Fetching AASX packages...")

    with get_client_from_context(ctx) as client:
        try:
            if all_pages:
                from basyx_client.pagination import iterate_pages

                packages = list(
                    iterate_pages(client.packages.list, limit=limit, aas_id=aas_id)
                )
            else:
                result = client.packages.list(limit=limit, cursor=cursor, aas_id=aas_id)
                packages = result.result

            format_output(
                packages,
                columns=[
                    ("package_id", "Package ID"),
                    ("aas_ids", "AAS IDs"),
                ],
                title="AASX Packages",
                extract_fn=_extract_package_summary,
            )
        except Exception as e:
            print_error(f"Failed to list packages: {e}")
            raise typer.Exit(1)


@app.command("get")
def get_package(
    ctx: typer.Context,
    package_id: str = typer.Argument(..., help="Package identifier"),
) -> None:
    """Get AASX package information."""
    print_verbose(ctx, f"Fetching package info: {package_id}")

    with get_client_from_context(ctx) as client:
        try:
            info = client.packages.get_info(package_id)
            format_output(info, title="AASX Package Info")
        except Exception as e:
            print_error(f"Failed to get package info: {e}")
            raise typer.Exit(1)


@app.command("download")
def download_package(
    ctx: typer.Context,
    package_id: str = typer.Argument(..., help="Package identifier"),
    output: Path = typer.Option(
        None,
        "--output",
        "-o",
        help="Output file path (defaults to {package_id}.aasx)",
    ),
) -> None:
    """Download an AASX package."""
    print_verbose(ctx, f"Downloading package: {package_id}")

    output_path = output or Path(f"{package_id}.aasx")

    with get_client_from_context(ctx) as client:
        try:
            content = client.packages.download(package_id)
            with open(output_path, "wb") as f:
                f.write(content)
            print_success(f"Downloaded package to: {output_path}")
            console.print(f"[dim]Size: {len(content)} bytes[/dim]")
        except Exception as e:
            print_error(f"Failed to download package: {e}")
            raise typer.Exit(1)


@app.command("upload")
def upload_package(
    ctx: typer.Context,
    file: Path = typer.Argument(
        ...,
        help="Path to AASX file",
        exists=True,
        readable=True,
    ),
    aas_id: Optional[str] = typer.Option(
        None, "--aas-id", help="Associate with specific AAS ID"
    ),
) -> None:
    """Upload an AASX package."""
    print_verbose(ctx, f"Uploading package: {file}")

    with get_client_from_context(ctx) as client:
        try:
            with open(file, "rb") as f:
                content = f.read()

            result = client.packages.upload(
                content,
                filename=file.name,
                aas_id=aas_id,
            )
            print_success(f"Uploaded package: {result.get('packageId', 'unknown')}")
            format_output(result, extract_fn=_extract_package_summary)
        except Exception as e:
            print_error(f"Failed to upload package: {e}")
            raise typer.Exit(1)


@app.command("delete")
def delete_package(
    ctx: typer.Context,
    package_id: str = typer.Argument(..., help="Package identifier"),
    force: bool = typer.Option(False, "--force", "-f", help="Skip confirmation"),
) -> None:
    """Delete an AASX package."""
    if not force:
        confirm = typer.confirm(f"Delete package '{package_id}'?")
        if not confirm:
            print_error("Aborted")
            raise typer.Exit(0)

    print_verbose(ctx, f"Deleting package: {package_id}")

    with get_client_from_context(ctx) as client:
        try:
            client.packages.delete(package_id)
            print_success(f"Deleted package: {package_id}")
        except Exception as e:
            print_error(f"Failed to delete package: {e}")
            raise typer.Exit(1)
