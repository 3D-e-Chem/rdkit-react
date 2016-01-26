# Copyright 2013 Netherlands eScience Center
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import argparse
import copy
import sys
from rdkit import Chem
from rdkit.Chem import AllChem


def main(argv=sys.argv[1:]):
    parser = argparse.ArgumentParser()
    parser.add_argument("--smarts", type=argparse.FileType('r'), help="File with reactions in SMART format", required=True)
    parser.add_argument("input", type=argparse.FileType('r'), help="Input SD file (use - for stdin)")
    parser.add_argument("output", type=argparse.FileType('w'), help="Output SD file (use - for stdout)")
    args = parser.parse_args(argv)

    smarts_file = args.smarts
    reactions = []
    with smarts_file as f:
        for line in f:
            cols = line.split()
            if len(cols) < 1:
                continue
            # cols[0] = smart, cols[1:] = comments
            reaction = AllChem.ReactionFromSmarts(cols[0])
            reactions.append(reaction)

    writer = Chem.SDWriter(args.output)
    writer.SetKekulize(False)
    reactants = Chem.ForwardSDMolSupplier(args.input)
    for reactant in reactants:
        reactant_name = reactant.GetProp("_Name")
        reactant.SetProp("_Name", "{}_frag1".format(reactant_name))
        writer.write(reactant)
        frag_counter = 2
        for reaction in reactions:
            products = reaction.RunReactants([reactant])
            for product in products:
                frags = (Chem.GetMolFrags(product[0], asMols=True))
                for frag in frags:
                    prod = copy.copy(frag)
                    prod.SetProp("_Name", "{}_frag{}".format(reactant_name, frag_counter))
                    writer.write(prod)
                    frag_counter += 1
