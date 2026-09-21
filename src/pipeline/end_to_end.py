"""
End-to-end pipeline: Video source → Detection → Stage1 → Stage2 → Event Engine → DB.
"""
import argparse
import pathlib
from omegaconf import OmegaConf
from loguru import logger


def parse_args():
    parser = argparse.ArgumentParser(description="Incident Detection Pipeline")
    parser.add_argument("--config", type=str, default="configs/pipeline.yaml")
    parser.add_argument("--source", type=str, default=None,
                        help="Override source path from config")
    return parser.parse_args()


def run(cfg):
    logger.info(f"Pipeline starting | source={cfg.source.path}")

    # TODO (Nguyên): plug in detection_tracking module
    # TODO (Nguyên): plug in stage1_rule_engine
    # TODO (Nguyên): plug in stage2_classifier
    # TODO (Son):    plug in flood_model
    # TODO (Lãnh):   plug in event_engine + database writer

    logger.info("Pipeline finished.")


def main():
    args = parse_args()
    cfg = OmegaConf.load(args.config)
    if args.source:
        cfg.source.path = args.source
    run(cfg)


if __name__ == "__main__":
    main()
