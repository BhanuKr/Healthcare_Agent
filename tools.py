from langchain.tools import BaseTool


class SpecialistInfoTool(BaseTool):
    name: str = "SpecialistInfoTool"
    description: str = "Provides info about a medical specialist based on the name."

    def _run(self, specialist_name: str) -> str:
        info = {
            "Cardiologist": (
                """ Cardiologist: A medical doctor who specializes in diagnosing, treating, and preventing diseases of the heart and blood vessels. 
                They manage conditions like high blood pressure, arrhythmias, heart failure, coronary artery disease, and congenital heart defects. 
                They may also perform diagnostic procedures such as ECGs, echocardiograms, and cardiac catheterization."""
            ),

            "Neurologist": (
                """Neurologist: A specialist in disorders of the nervous system, including the brain, spinal cord, and peripheral nerves. 
                They treat conditions such as migraines, epilepsy, stroke, multiple sclerosis, Parkinson’s disease, and neuropathies. 
                They may perform neurological exams, imaging analysis, and nerve conduction studies to evaluate symptoms like dizziness, seizures, or numbness."""
            ),

            "Gastroenterologist": (
                """Gastroenterologist: A doctor who focuses on the digestive system and its disorders. 
                They treat issues involving the esophagus, stomach, intestines, liver, pancreas, and gallbladder. 
                Common conditions include acid reflux, ulcers, irritable bowel syndrome (IBS), Crohn’s disease, hepatitis, and gastrointestinal bleeding. 
                They often perform endoscopy and colonoscopy for diagnosis and treatment."""
            ),

            "Dermatologist": (
                """Dermatologist: A specialist in skin, hair, and nail health. 
                They diagnose and treat skin conditions like eczema, acne, psoriasis, fungal infections, skin allergies, and skin cancer. 
                They also perform procedures such as biopsies, mole removal, and cosmetic treatments including Botox, fillers, and laser therapy."""
            ),

            "Pulmonologist": (
                """Pulmonologist: A doctor specializing in diseases of the respiratory system, including the lungs and bronchial tubes. 
                They manage conditions like asthma, chronic obstructive pulmonary disease (COPD), pneumonia, lung infections, sleep apnea, and pulmonary fibrosis. 
                They may use pulmonary function tests, chest imaging, and bronchoscopy for diagnosis and monitoring."""
            ),

            "Orthopedist": (
                """Orthopedist: A physician who specializes in the musculoskeletal system — bones, joints, muscles, ligaments, tendons, and spine. 
                They diagnose and treat conditions like arthritis, fractures, sprains, joint pain, scoliosis, and sports injuries. 
                Orthopedists may offer physical therapy, medications, or perform surgeries such as joint replacements and arthroscopic procedures."""
            ),

            "General Practitioner": (
                """General Practitioner: A primary care doctor who provides broad medical care for all age groups. 
                They evaluate general symptoms, manage chronic diseases like diabetes or hypertension, and provide preventative care including vaccinations and health screenings. 
                They serve as the first point of contact and may refer patients to specialists when further evaluation is needed."""
            )
        }

        return info.get(specialist_name, f"No information available for {specialist_name}.")

    def _arun(self, specialist_name: str) -> str:
        raise NotImplementedError("Async not supported.")