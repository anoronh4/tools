import json
import os
from pathlib import Path

import pytest

from nf_core.components.snapshot_generator import ComponentTestSnapshotGenerator

from ..utils import GITLAB_NFTEST_BRANCH, GITLAB_URL, set_wd


def test_generate_snapshot_module(self):
    """Generate the snapshot for a module in nf-core/modules clone"""
    with set_wd(self.nfcore_modules):
        snap_generator = ComponentTestSnapshotGenerator(
            component_type="modules",
            component_name="fastqc",
            no_prompts=True,
            remote_url=GITLAB_URL,
            branch=GITLAB_NFTEST_BRANCH,
        )
        snap_generator.run()

        snap_path = Path("modules", "nf-core-test", "fastqc", "tests", "main.nf.test.snap")
        assert snap_path.exists()

        with open(snap_path, "r") as fh:
            snap_content = json.load(fh)
        assert "versions" in snap_content
        assert "content" in snap_content["versions"]
        assert "versions.yml:md5,e1cc25ca8af856014824abd842e93978" in snap_content["versions"]["content"][0]


def test_generate_snapshot_subworkflow(self):
    """Generate the snapshot for a subworkflows in nf-core/modules clone"""
    with set_wd(self.nfcore_modules):
        snap_generator = ComponentTestSnapshotGenerator(
            component_type="subworkflows",
            component_name="bam_sort_stats_samtools",
            no_prompts=True,
            remote_url=GITLAB_URL,
            branch=GITLAB_NFTEST_BRANCH,
        )
        snap_generator.run()

        snap_path = Path("subworkflows", "nf-core-test", "bam_sort_stats_samtools", "tests", "main.nf.test.snap")
        assert snap_path.exists()

        with open(snap_path, "r") as fh:
            snap_content = json.load(fh)
        assert "test_bam_sort_stats_samtools_paired_end_flagstats" in snap_content
        assert (
            "test.flagstat:md5,4f7ffd1e6a5e85524d443209ac97d783"
            in snap_content["test_bam_sort_stats_samtools_paired_end_flagstats"]["content"][0][0]
        )
        assert "test_bam_sort_stats_samtools_paired_end_idxstats" in snap_content
        assert (
            "test.idxstats:md5,df60a8c8d6621100d05178c93fb053a2"
            in snap_content["test_bam_sort_stats_samtools_paired_end_idxstats"]["content"][0][0]
        )


def test_update_snapshot_module(self):
    """Update the snapshot of a module in nf-core/modules clone"""
    original_timestamp = "2023-10-18T11:02:55.420631681"

    with set_wd(self.nfcore_modules):
        snap_generator = ComponentTestSnapshotGenerator(
            component_type="modules",
            component_name="bwa/mem",
            no_prompts=True,
            remote_url=GITLAB_URL,
            branch=GITLAB_NFTEST_BRANCH,
            update=True,
        )
        snap_generator.run()

        snap_path = Path("modules", "nf-core-test", "bwa", "mem", "tests", "main.nf.test.snap")
        assert snap_path.exists()

        with open(snap_path, "r") as fh:
            snap_content = json.load(fh)
        assert "Single-End" in snap_content
        assert snap_content["Single-End"]["timestamp"] != original_timestamp


def test_test_not_found(self):
    """Generate the snapshot for a module in nf-core/modules clone which doesn't contain tests"""
    with set_wd(self.nfcore_modules):
        snap_generator = ComponentTestSnapshotGenerator(
            component_type="modules",
            component_name="fastp",
            no_prompts=True,
            remote_url=GITLAB_URL,
            branch=GITLAB_NFTEST_BRANCH,
        )
        with pytest.raises(UserWarning) as e:
            snap_generator.run()
            assert "Test file 'main.nf.test' not found" in e


def test_unstable_snapshot(self):
    """Generate the snapshot for a module in nf-core/modules clone with unstable snapshots"""
    with set_wd(self.nfcore_modules):
        snap_generator = ComponentTestSnapshotGenerator(
            component_type="modules",
            component_name="kallisto/quant",
            no_prompts=True,
            remote_url=GITLAB_URL,
            branch=GITLAB_NFTEST_BRANCH,
        )
        with pytest.raises(UserWarning) as e:
            snap_generator.run()
            assert "nf-test snapshot is not stable" in e
