




def parallel_annotation_efficient(self, n_processes, verbose=1):
    self.verbose = verbose
    samples = self.mapping.keys()
    process_mapping = dict.fromkeys(['process_%i' % i for i in range(n_processes)], 0)

    for sample in samples:
        list_tupls = self.get_sample_csv_vcf_tuple(sample)
        for tpl in list_tupls:
            hgvs = HgvsParser(tpl[1])
            csv_parsing = TxtParser(tpl[2])

        self.pooling(n_processes, list_tupls)
        logger.info('Completed annotation and parsing for variants in sample %s' % sample)


def _variant_parsing_efficitent(self, maps):
    hgvs = HgvsParser(maps[1])
    csv_parsing = TxtParser(maps[2])

    variant_buffer = []
    n_vars = 0

    # for i in n_processes:
    #    chunk_n =

    while csv_parsing.num_lines > self.step * self.chunksize:

        list_hgvs_ids = hgvs.get_variants_from_vcf(self.step)
        myvariants_variants = self.get_dict_myvariant(list_hgvs_ids, self.verbose, maps[0])

        offset = len(list_hgvs_ids) - self.chunksize
        csv_variants = csv_parsing.open_and_parse_chunks(self.step, build_ver=self.buildver, offset=offset)

        merged_list = []
        for i, _ in enumerate(myvariants_variants):
            merged_list.append(
                self.merge_dict_lists(myvariants_variants[i], csv_variants[i][j]) for j in csv_variants[i])

        variant_buffer.extend(merged_list)
        n_vars += len(merged_list)
        if self.verbose >= 1:
            logger.info('Gathered %i variants so far for sample %s, vcf file %s' % (n_vars, maps[0], maps[1]))
        self.step += 1

        if len(merged_list) < self.chunksize:
            self._last_round = True

        if (len(variant_buffer) > self._buffer_len) or self._last_round:
            logging.info('Parsing Buffer...')
            self.export(variant_buffer)
            variant_buffer = []

            if self._last_round:
                self.completed_jobs[maps[0]] += 1
                return self.completed_jobs

    return self.completed_jobs