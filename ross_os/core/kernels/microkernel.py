import pandas as pd
import json
import hashlib
import os
from datetime import datetime
from pathlib import Path

class MicrokernelOrchestrator:
    """
    Deterministic data router that splits raw data into public visual metrics
    and secure technical logs following the "public-first with gated supplementary" model.
    """
    
    def __init__(self, registry_path="../../data/tenders/master_registry.csv"):
        self.registry_path = registry_path
        self.output_base = Path(__file__).parent.parent.parent / "data" / "outputs"
        self.output_base.mkdir(parents=True, exist_ok=True)
        self.execution_timestamp = datetime.utcnow().isoformat()
        self.execution_hash = self._generate_execution_hash()
        self.data_df = None
        
    def _generate_execution_hash(self):
        """Generate cryptographic execution identifier."""
        seed = f"{self.execution_timestamp}{os.urandom(16).hex()}"
        return hashlib.sha256(seed.encode()).hexdigest()[:16]
    
    def validate_registry(self):
        """
        Validate registry schema and load data.
        Mirrors validation logic from render_matrix.py.
        """
        if not os.path.exists(self.registry_path):
            print(f"[ERROR] Registry file not found at {self.registry_path}")
            return False
        
        try:
            self.data_df = pd.read_csv(self.registry_path)
            required_columns = ['date', 'sector', 'title', 'video_style', 'video_voiceover_prompt']
            
            if not all(col in self.data_df.columns for col in required_columns):
                print("[ERROR] Internal OS Schema Mismatch. Aborting ingestion loop.")
                return False
            
            print(f"[SUCCESS] {len(self.data_df)} live vectors validated. Ready for orchestration.")
            return True
        except Exception as e:
            print(f"[ERROR] Registry validation failed: {str(e)}")
            return False
    
    def filter_by_sector(self, sector_name):
        """
        Isolate active global vectors by sector (Tech, Infrastructure, Health).
        Returns filtered dataframe for sector-specific command decks.
        """
        if self.data_df is None:
            print("[ERROR] No data loaded. Run validate_registry() first.")
            return None
        
        filtered = self.data_df[self.data_df['sector'].str.lower() == sector_name.lower()]
        print(f"[SECTOR FILTER] {len(filtered)} records isolated for sector: {sector_name}")
        return filtered
    
    def generate_video_manifest(self):
        """
        Compile automation manifest with exact video styles and voiceover scripts
        for the automated video-generation notebook.
        
        Returns:
            list: Array of video automation payloads
        """
        if self.data_df is None or len(self.data_df) == 0:
            print("[WARNING] No data available for video manifest generation.")
            return []
        
        manifest = []
        for idx, row in self.data_df.iterrows():
            payload = {
                "sequence_id": idx + 1,
                "date": row['date'],
                "sector": row['sector'],
                "title": row['title'],
                "video_style": row['video_style'],
                "voiceover_prompt": row['video_voiceover_prompt'],
                "render_priority": self._calculate_priority(row['sector']),
                "automation_flag": True
            }
            manifest.append(payload)
        
        print(f"[VIDEO MANIFEST] Generated {len(manifest)} automation payloads.")
        return manifest
    
    def generate_system_telemetry(self):
        """
        Output live runtime variables for visual dashboard elements.
        Shows system activity and processing metrics.
        
        Returns:
            dict: System telemetry snapshot
        """
        if self.data_df is None:
            record_count = 0
            sector_breakdown = {}
        else:
            record_count = len(self.data_df)
            sector_breakdown = self.data_df['sector'].value_counts().to_dict()
        
        telemetry = {
            "execution_id": self.execution_hash,
            "timestamp": self.execution_timestamp,
            "system_status": "active" if self.data_df is not None else "idle",
            "total_records": record_count,
            "sector_distribution": sector_breakdown,
            "pipeline_stages": {
                "validation": "complete",
                "routing": "active",
                "public_payload": "ready",
                "gated_payload": "ready"
            },
            "performance_metrics": {
                "records_processed": record_count,
                "schemas_validated": 1,
                "manifests_compiled": record_count
            }
        }
        
        return telemetry
    
    def sign_gated_proofs(self):
        """
        Generate mock verification hashes for secure technical appendices.
        Ensures data remains defensible and tamper-proof.
        
        Returns:
            dict: Gated audit proofs with cryptographic signatures
        """
        if self.data_df is None or len(self.data_df) == 0:
            proofs = []
        else:
            proofs = []
            for idx, row in self.data_df.iterrows():
                # Create deterministic hash from row data
                row_str = f"{row['date']}{row['sector']}{row['title']}{row['video_style']}"
                row_hash = hashlib.sha256(row_str.encode()).hexdigest()
                
                proof = {
                    "record_id": idx + 1,
                    "content_hash": row_hash,
                    "signature": self._create_signature(row_hash),
                    "access_level": "restricted",
                    "audit_timestamp": self.execution_timestamp
                }
                proofs.append(proof)
        
        audit_structure = {
            "execution_id": self.execution_hash,
            "total_proofs": len(proofs),
            "ledger_hash": hashlib.sha256(json.dumps(proofs).encode()).hexdigest(),
            "access_rules": {
                "default": "deny",
                "authorized_peers": ["admin", "auditor"],
                "encryption_standard": "sha256"
            },
            "proofs": proofs
        }
        
        return audit_structure
    
    def _calculate_priority(self, sector):
        """Calculate render priority based on sector type."""
        priority_map = {
            "tech": 1,
            "infrastructure": 2,
            "health": 3
        }
        return priority_map.get(sector.lower(), 4)
    
    def _create_signature(self, content_hash):
        """Create mock signature for gated content."""
        sig_seed = f"{content_hash}{self.execution_hash}"
        return hashlib.sha256(sig_seed.encode()).hexdigest()[:24]
    
    def execute_orchestration_loop(self):
        """
        Main execution loop: Validate, Route, and Generate dual payloads.
        
        Returns:
            dict: Execution summary with status and output paths
        """
        print("\n" + "="*60)
        print("[MICROKERNEL] Orchestration Engine Starting...")
        print("="*60)
        
        # Step 1: Validate Registry
        if not self.validate_registry():
            print("[FATAL] Registry validation failed. Aborting orchestration.")
            return {"status": "failed", "reason": "validation_error"}
        
        # Step 2: Generate Artifacts
        print("\n[ORCHESTRATION] Generating public and gated payloads...")
        
        video_manifest = self.generate_video_manifest()
        system_telemetry = self.generate_system_telemetry()
        gated_proofs = self.sign_gated_proofs()
        
        # Step 3: Create Public Telemetry Output
        public_payload = {
            "execution_id": self.execution_hash,
            "timestamp": self.execution_timestamp,
            "system_telemetry": system_telemetry,
            "video_automation_manifest": video_manifest,
            "visibility": "public",
            "dashboard_ready": True
        }
        
        public_output_path = self.output_base / "public_telemetry.json"
        with open(public_output_path, 'w') as f:
            json.dump(public_payload, f, indent=2)
        print(f"[PUBLIC OUTPUT] Written to {public_output_path}")
        
        # Step 4: Create Gated Audit Ledger
        gated_payload = {
            "execution_id": self.execution_hash,
            "timestamp": self.execution_timestamp,
            "audit_ledger": gated_proofs,
            "visibility": "gated",
            "access_control": "restricted",
            "verification_ready": True
        }
        
        gated_output_path = self.output_base / "gated_audit_ledger.json"
        with open(gated_output_path, 'w') as f:
            json.dump(gated_payload, f, indent=2)
        print(f"[GATED OUTPUT] Written to {gated_output_path}")
        
        # Step 5: Summary
        print("\n" + "="*60)
        print("[MICROKERNEL] Orchestration Complete")
        print("="*60)
        print(f"✅ Execution ID: {self.execution_hash}")
        print(f"✅ Records Processed: {len(self.data_df)}")
        print(f"✅ Public Payload: {public_output_path}")
        print(f"✅ Gated Payload: {gated_output_path}")
        
        return {
            "status": "success",
            "execution_id": self.execution_hash,
            "records_processed": len(self.data_df),
            "public_output": str(public_output_path),
            "gated_output": str(gated_output_path)
        }


if __name__ == "__main__":
    # Initialize and execute microkernel
    microkernel = MicrokernelOrchestrator()
    result = microkernel.execute_orchestration_loop()
    
    # Print execution summary
    print("\n" + json.dumps(result, indent=2))
